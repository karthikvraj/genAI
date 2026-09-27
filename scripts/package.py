"""Build source-only project downloads and a portfolio bundle; never publish remotely."""
from __future__ import annotations
import hashlib
import json
import platform
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import numpy
import scipy
import sklearn
from reliable_ai_lab import __version__
from reliable_ai_lab.registry import PROJECTS, get_project

DETAILS = {
'evidence-gate': ('LLM answers can cite real documents while introducing unsupported numbers or claims.',
 'Resolve citations, split cited text into sentences, rank lexical overlap, and flag unmatched numbers and negation changes. Keep the exact supporting excerpt.',
 'Replace lexical screening with a separately evaluated entailment model; add multilingual, unit-conversion and adversarial datasets.',
 ['sources: unique id/text records','claims: text plus source_ids','threshold: lexical similarity cutoff, default 0.35'],
 'Try changing 128 requests to 256 requests, removing a citation, or reversing a negation.'),
'budget-rag': ('A fixed number of retrieved chunks can exceed a context budget or repeat the same information.',
 'Use TF-IDF relevance, diversity penalties and a length-aware greedy selector. Compare its word count with a fixed-top-three retrieval baseline.',
 'Add tokenizer-specific budgets, dense retrieval and answer-quality evaluation before claiming context or cost improvements.',
 ['documents: unique id/text records','query: nonempty question','word_budget: positive whitespace-word limit','expected_source_ids: optional labeled source set'],
 'Reduce word_budget from 38 to 15. Compare selected_words with fixed_top3_words.'),
'repair-agent': ('A plan that looks plausible can contain invented references or unauthorized actions.',
 'Validate references, required fields and an action allowlist. Run a bounded repair loop, detect repeated plans and keep a hash-linked audit trace. All plans require human review.',
 'Evaluate the optional local model adapter on adversarial plans. Add authenticated audit storage; do not confuse schema validation with reasoning correctness.',
 ['sources: unique id/text records','plan: hypothesis/source_ids/actions/human_approval_required','max_attempts: 1..5'],
 'Delete hypothesis. The agent should stop rather than manufacture one. The optional Ollama path is explicit opt-in.'),
'incident-room': ('On-call engineers need evidence that connects a telemetry change to relevant operational guidance.',
 'Fit an Isolation Forest on the reference window, compute robust median shifts and retrieve relevant runbook text. Combine observations in a non-executing triage report.',
 'Integrate approved telemetry schemas, time-aware validation and operator feedback. Evaluate against labeled incidents before paging anyone.',
 ['baseline and current: numeric matrices with matching columns','feature_names: unique ordered names','runbooks: unique id/text records'],
 'Set current equal to baseline. Median-shift findings should disappear.'),
'inference-twin': ('Capacity loss can push a service from manageable waiting time into an unstable queue.',
 'Simulate Poisson arrivals and exponential service on identical servers. Train a random-forest latency surrogate on independent simulated operating points and report held-out MAE against a constant predictor.',
 'Calibrate to measured inference traces, batching and prefill/decode behavior; add repeated simulation intervals and out-of-distribution checks.',
 ['arrival_rps: positive arrival rate','service_ms: mean service time in milliseconds','servers and lost_servers: integer capacity','requests and seed: finite simulation controls'],
 'Change lost_servers from 3 to 0. Read offered_utilization and steady_state_possible before interpreting p95 latency.'),
'gpu-guard': ('A useful GPU alert needs a healthy reference, a defensible threshold, and visible false positives.',
 'Split reference data into fitting and calibration sets. Fit Isolation Forest, compute rank-based anomaly p-values, and report large robust metric deviations. Optional labels are used only for evaluation.',
 'Use real approved telemetry, temporally aware calibration and fleet-wide alert budgeting. Validate GPU-specific failure modes.',
 ['reference and current: matching numeric matrices','feature_names: unique ordered metric names','alpha: per-sample rank threshold','labels: optional binary current-window labels'],
 'Set alpha to 0.001. The sample calibration set cannot attain that significance level, and no row should be flagged.'),
'evalforge': ('A model comparison can hide uncertainty, confidence errors and the cost of abstaining.',
 'Evaluate saved answers with normalized exact match and token F1. Compute Brier score, ten-bin calibration error, risk/coverage and paired bootstrap intervals. Preserve per-group results.',
 'Add independently labeled semantic evaluation, clustered bootstrap for related prompts and held-out threshold selection.',
 ['records: unique id/reference/answer/confidence records','baseline_answer: present on all rows or none','latency_ms and cost_usd: caller-supplied measurements','group: optional evaluation slice'],
 'Change an incorrect answer with high confidence. Watch calibration and Brier score rather than just aggregate accuracy.'),
'research-lens': ('A research note should let the reader inspect the exact text behind every excerpt.',
 'Retrieve and deduplicate source sentences, attach stable source identifiers and SHA-256 hashes, expose uncovered query terms, and abstain when lexical evidence is absent.',
 'Add approved document parsers, page offsets, semantic retrieval and an evidence-quality assessment dataset.',
 ['documents: unique id/text records','query: nonempty research question','max_excerpts: 1..20','minimum_similarity: retrieval cutoff'],
 'Ask a question unrelated to the supplied corpus. The tool should return an empty extractive note.'),
 'topology-rca': ('The loudest downstream alert is not necessarily the best explanation of an incident.',
 'Use a dependency graph to construct single-fault likelihoods, condition on both positive and negative symptoms, and rank hypotheses including no_fault. Optional labeled cases update likelihoods with smoothing.',
 'Evaluate on independent labeled incidents, account for symptom dependence and multiple simultaneous faults, and test probability calibration.',
 ['nodes: unique component names','edges: dependency-to-consumer pairs','observed: component-to-boolean symptom mapping','training_cases and priors: optional labeled model inputs'],
 'Mark every observed node healthy. Compare no_fault against the original shared-fabric hypothesis.'),
'drift-radar': ('Inputs can change after deployment without an immediate visible change in aggregate metrics.',
 'Run per-feature two-sample KS tests with Holm correction and a standardized Wasserstein effect filter. Separately train a reference/current classifier and report its held-out AUC.',
 'Add time-aware splits, sequential false-alert controls and labeled outcome evaluation; input drift alone is not concept drift.',
 ['reference and current: matching numeric matrices','feature_names: ordered unique feature names','alpha and minimum_effect: statistical and practical filters'],
 'Set current equal to reference. Feature-shift flags should disappear.')
}


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False)+'\n', encoding='utf-8')


def readme(name, result, standalone=False):
    meta = PROJECTS[name]
    problem, method, roadmap, inputs, experiment = DETAILS[name]
    prefix = '' if standalone else '../../'
    fields = '\n'.join('- ' + value for value in inputs)
    limitations = '\n'.join('- ' + value for value in result['limitations'])
    metrics = '\n'.join(
        f'| {key} | {value:.6g} |' if isinstance(value, float)
        else f'| {key} | {value} |'
        for key, value in result['metrics'].items()
    )
    links = '' if standalone else (
        f'[Lab README](../../README.md) · '
        f'[Download ZIP](../../../../releases/download/reliable-ai-lab-v{__version__}/'
        f'{name}-v{__version__}.zip)\n'
    )
    location = 'From the extracted project directory:' if standalone else 'From the repository root:'
    return f'''# {meta['title']}

{meta['tagline']}

Karthik Coimbatore Varadaraj · v{__version__}

{links}
## What it does

{problem}

{method}

## Run

{location}

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m reliable_ai_lab demo {name}
python -m reliable_ai_lab sample {name} --output input.json
python -m reliable_ai_lab run {name} --input input.json --output result.json
python -m reliable_ai_lab serve
```

On Windows, activate with `.venv\\Scripts\\activate`. The browser app runs at `http://127.0.0.1:8765`. Default examples need no API key or GPU; install the Python dependencies first.

## Inputs

{fields}

The `sample` command writes a valid input. See `run()` in the implementation for parameter limits. Matrices use rows for observations and columns in `feature_names` order.

## Try a change

{experiment}

## Example results

Seed 7, using synthetic or hand-authored data. These results illustrate the code; they are not production benchmarks. Small numeric differences can occur across dependency versions.

| Metric | Result |
|---|---:|
{metrics}

## Code and tests

[Implementation]({prefix}reliable_ai_lab/{meta['module']}.py) · [Tests]({prefix}tests/test_{meta['module']}.py)

## Limitations

{limitations}

## Next work

{roadmap}

## Data and license

The examples contain no employer or customer data. The lab code is MIT-licensed; see [LICENSE]({prefix}LICENSE) and [license scope]({prefix}LICENSE_SCOPE.md). Check third-party data and model licenses before using them.
'''


def zip_directory(folder, destination, label):
    with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for file in sorted(folder.rglob('*')):
            if folder == ROOT and file.relative_to(folder).parts[0] not in {'reliable_ai_lab','tests','scripts','projects','docs','.github','pyproject.toml','README.md','LICENSE','LICENSE_SCOPE.md','SECURITY.md','CONTRIBUTING.md','CITATION.cff','.gitignore'}:
                continue
            if file.is_file() and not any(part in {'__pycache__','.pytest_cache','.git','dist','build'} or part.endswith('.egg-info') for part in file.relative_to(folder).parts):
                info=zipfile.ZipInfo(str(Path(label)/file.relative_to(folder)),date_time=(2026,9,26,0,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED
                info.external_attr=0o100644 << 16
                archive.writestr(info,file.read_bytes())


def build(out=None):
    out=Path(out) if out else ROOT/'dist';out.mkdir(parents=True,exist_ok=True)
    env={'python':platform.python_version(),'numpy':numpy.__version__,'scipy':scipy.__version__,'scikit-learn':sklearn.__version__}
    results={};inputs={}
    for name in PROJECTS:
        module=get_project(name);inputs[name]=module.sample(7);results[name]=module.run(inputs[name])
        directory=ROOT/'projects'/name;directory.mkdir(parents=True,exist_ok=True)
        (directory/'README.md').write_text(readme(name,results[name]),encoding='utf-8')
        dump(directory/'examples/input.json',inputs[name]);dump(directory/'examples/result.json',results[name])
    dump(ROOT/'docs/environment.json',env)
    dump(ROOT/'docs/demo-results.json',{'seed':7,'data':'synthetic','environment':env,'results':results})
    artifacts=[]
    for name,meta in PROJECTS.items():
        with tempfile.TemporaryDirectory() as tmp:
            stage=Path(tmp)
            package=stage/'reliable_ai_lab';package.mkdir()
            for filename in ['__init__.py','common.py','__main__.py','server.py',meta['module']+'.py']:
                shutil.copy2(ROOT/'reliable_ai_lab'/filename,package/filename)
            registry=(ROOT/'reliable_ai_lab/registry.py').read_text()
            start=registry.index('PROJECTS = ');end=registry.index('\n\n\ndef get_project',start)
            registry=registry[:start]+'PROJECTS = '+repr({name:meta})+registry[end:]
            (package/'registry.py').write_text(registry)
            shutil.copytree(ROOT/'reliable_ai_lab/web',package/'web')
            page=package/'web/index.html';page.write_text(page.read_text().replace('Ten projects covering model outputs, retrieval and infrastructure behavior.',meta['title']+': '+meta['tagline']))
            config=(ROOT/'pyproject.toml').read_text().replace('name = "kv-reliable-ai-lab"',f'name = "kv-{name}"')
            (stage/'pyproject.toml').write_text(config)
            (stage/'README.md').write_text(readme(name,results[name],True))
            for filename in ['LICENSE','LICENSE_SCOPE.md','SECURITY.md','CONTRIBUTING.md','.gitignore']:
                if (ROOT/filename).exists():shutil.copy2(ROOT/filename,stage/filename)
            tests=stage/'tests';tests.mkdir()
            for filename in ['test_contracts.py','test_server_cli.py',f'test_{meta["module"]}.py']:
                shutil.copy2(ROOT/'tests'/filename,tests/filename)
            dump(stage/'examples/input.json',inputs[name]);dump(stage/'examples/result.json',results[name]);dump(stage/'environment.json',env)
            filename=f'{name}-v{__version__}.zip';zip_directory(stage,out/filename,f'{name}-v{__version__}');artifacts.append(out/filename)
    # Static replay is explicitly labeled: changing inputs does not run Python in this HTML file.
    page=(ROOT/'reliable_ai_lab/web/index.html').read_text()
    page=page.replace('CPU-only demo','Recorded sample').replace('Run experiment →','Replay recorded result →').replace('Running the local experiment…','Loading the recorded result…')
    page=page.replace('01 / editable input · JSON','01 / recorded input · JSON').replace('Ready. Run the example or edit the JSON.','Ready. Replay this recorded sample.')
    page=page.replace('<textarea id="input"','<textarea readonly id="input"')
    page=page.replace('Inputs stay with this local Python process. Use approved, non-sensitive data.','Read-only sample. Run the Python playground to edit inputs and compute new results.')
    page=page.replace('Edit the JSON, run the project and review the result.','Recorded results. Run the Python package to use your own inputs.')
    page=page.replace('Synthetic data. Default runs need no API key or GPU and make no infrastructure changes.','Saved outputs from synthetic examples. This gallery does not run Python or a model.')
    old="async function request(url,options){let r=await fetch(url,options);let d=await r.json();if(!r.ok)throw Error(d.error||'Request failed');return d}"
    data=json.dumps({'projects':PROJECTS,'inputs':inputs,'results':results},separators=(',',':'),allow_nan=False).replace('<','\\u003c')
    new='const RECORDED='+data+";async function request(url,options){if(url==='/api/projects')return RECORDED.projects;let name=url.split('/').pop();return url.startsWith('/api/sample/')?RECORDED.inputs[name]:RECORDED.results[name]}"
    assert old in page
    page=page.replace(old,new)
    (out/'reliable-ai-lab-demo-gallery.html').write_text(page,encoding='utf-8');artifacts.append(out/'reliable-ai-lab-demo-gallery.html')
    master=out/f'reliable-ai-lab-v{__version__}.zip'
    zip_directory(ROOT,master,f'reliable-ai-lab-v{__version__}');artifacts.append(master)
    artifacts.extend(sorted(out.glob(f'*-{__version__}-*.whl')))
    manifest={'version':__version__,'synthetic_demo_seed':7,'environment':env,'artifacts':[]}
    for path in artifacts:
        manifest['artifacts'].append({'file':path.name,'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    dump(out/'manifest.json',manifest)
    (out/'SHA256SUMS.txt').write_text(''.join(f"{a['sha256']}  {a['file']}\n" for a in manifest['artifacts']))
    print(json.dumps(manifest,indent=2))
    return manifest

if __name__=='__main__':
    build(sys.argv[1] if len(sys.argv)>1 else None)
