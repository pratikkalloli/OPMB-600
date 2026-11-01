// Contribution-only structural audit. Does not run or replace Python tests.
const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'../../../..');
const base=__dirname;
const apps=JSON.parse(fs.readFileSync(path.join(base,'applications.json'),'utf8'));
const repos=JSON.parse(fs.readFileSync(path.join(base,'repository_manifest.json'),'utf8')).repositories;
const tasks=JSON.parse(fs.readFileSync(path.join(base,'task_manifest.json'),'utf8')).tasks;
const taskSchema=JSON.parse(fs.readFileSync(path.join(root,'benchmark/schemas/task.schema.json'),'utf8'));
const repoSchema=JSON.parse(fs.readFileSync(path.join(root,'benchmark/schemas/repository.schema.json'),'utf8'));
const globalTasks=JSON.parse(fs.readFileSync(path.join(root,'benchmark/manifests/tasks.json'),'utf8')).tasks;
const globalRepos=JSON.parse(fs.readFileSync(path.join(root,'benchmark/manifests/repositories.json'),'utf8')).repositories;
const errors=[], batches={B1:[321,370],B2:[371,420],B3:[421,470]};
const allocatedApps=new Set(apps.map(a=>a.id)),allocatedTasks=new Set(tasks.map(t=>t.task_id));
if(apps.length!==15||repos.length!==15||tasks.length!==150) errors.push('expected exactly 15 apps, 15 repo records, and 150 task records');
if(new Set(allocatedApps).size!==15||new Set(allocatedTasks).size!==150) errors.push('duplicate contribution IDs');
for(const r of globalRepos) if(allocatedApps.has(r.repository_id)) errors.push('repository ID collides with global manifest: '+r.repository_id);
for(const t of globalTasks) if(allocatedTasks.has(t.task_id)) errors.push('task ID collides with global manifest: '+t.task_id);
for(const r of repos) for(const field of repoSchema.required) if(!(field in r)) errors.push(r.repository_id+' missing repository schema field '+field);
for(const t of tasks) for(const field of taskSchema.required) if(!(field in t)) errors.push(t.task_id+' missing task schema field '+field);
for(const [batch,[start,end]] of Object.entries(batches)) {
  const selected=tasks.filter(t=>t.task_batch===batch);
  if(selected.length!==50) errors.push(batch+' must contain 50 tasks');
  for(let n=start;n<=end;n++) if(!allocatedTasks.has('OPMB-'+String(n).padStart(4,'0'))) errors.push(batch+' missing OPMB-'+String(n).padStart(4,'0'));
}
for(const app of apps) {
  const repo=repos.find(r=>r.repository_id===app.id), dir=path.join(root,'benchmark/repositories',app.id), own=tasks.filter(t=>t.repository_id===app.id);
  if(!repo||own.length!==10||repo.task_count!==10) errors.push(app.id+' does not have exactly ten tasks');
  const files=[`README.md`,`requirements.txt`,`pyproject.toml`,`src/${app.slug}/service.py`,`migrated_reference/${app.slug}_pqc/service.py`,`tests/test_${app.slug}.py`,`tests/test_${app.slug}_pqc.py`];
  for(const file of files) if(!fs.existsSync(path.join(dir,file))) errors.push(app.id+' missing '+file);
  const source=fs.existsSync(path.join(dir,files[3]))?fs.readFileSync(path.join(dir,files[3]),'utf8'):'';
  const ref=fs.existsSync(path.join(dir,files[4]))?fs.readFileSync(path.join(dir,files[4]),'utf8'):'';
  if(/\bRSA\b|OAEP|PSS|ECDSA|ECDH|X25519|X448/.test(ref)) errors.push(app.id+' PQC reference contains classical public-key patterns');
  for(const t of own) {
    if(!fs.existsSync(path.join(root,t.task_path,'task.json'))) errors.push(t.task_id+' task.json absent');
    else if(JSON.stringify(JSON.parse(fs.readFileSync(path.join(root,t.task_path,'task.json'),'utf8'))) !== JSON.stringify(t)) errors.push(t.task_id+' per-task record differs from contribution manifest');
    for(const rel of [...t.original_tests,...t.migration_tests]) if(!fs.existsSync(path.join(dir,rel))) errors.push(t.task_id+' references absent test '+rel);
    for(const fn of t.function_names) {
      if(!new RegExp('\\bdef\\s+'+fn+'\\s*\\(').test(source)) errors.push(t.task_id+' source function absent: '+fn);
      if(!new RegExp('\\bdef\\s+'+fn+'\\s*\\(').test(ref)) errors.push(t.task_id+' reference function absent: '+fn);
      for(const rel of [...t.original_tests,...t.migration_tests]) if(fs.existsSync(path.join(dir,rel))&&!fs.readFileSync(path.join(dir,rel),'utf8').includes(fn)) errors.push(t.task_id+' test does not mention '+fn);
    }
  }
}
if(new Set(tasks.map(t=>t.migration_objective)).size!==150) errors.push('duplicate task objectives');
const secret=/BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY|AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9]{20,}/;
for(const app of apps) for(const tree of ['src','migrated_reference','tests']) {
  const walk=p=>fs.readdirSync(p,{withFileTypes:true}).forEach(e=>{const f=path.join(p,e.name);if(e.isDirectory())walk(f);else if(secret.test(fs.readFileSync(f,'utf8')))errors.push('secret-like string in '+f);});
  walk(path.join(root,'benchmark/repositories',app.id,tree));
}
const report={status:errors.length?'FAIL':'PASS',method:'Node.js contribution-only structural/static audit; not Python schema execution or runtime tests',repositories:repos.length,tasks:tasks.length,task_range:[tasks[0]?.task_id,tasks.at(-1)?.task_id],batches:Object.fromEntries(Object.entries(batches).map(([b,[s,e]])=>[b,{repository_count:5,task_count:tasks.filter(t=>t.task_batch===b).length,range:['OPMB-'+String(s).padStart(4,'0'),'OPMB-'+String(e).padStart(4,'0')]}])),unique_task_ids:new Set(tasks.map(t=>t.task_id)).size===150,unique_objectives:new Set(tasks.map(t=>t.migration_objective)).size===150,global_id_collisions:errors.filter(e=>e.includes('collides')).length,errors};
fs.writeFileSync(path.join(base,'static_validation.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));
process.exitCode=errors.length?1:0;
