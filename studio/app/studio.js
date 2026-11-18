(() => {
  const $ = selector => document.querySelector(selector);
  const config = JSON.parse($('#studio-config').textContent);
  let library = {components:[]};
  let selectedId = new URLSearchParams(location.search).get('component');
  let versionId = null;
  let category = 'all';
  let view = 'preview';
  let width = 'fit';
  let sourceFile = 'source.html';
  let currentSource = '';
  let fingerprint = '';
  let previewKey = '';
  let sourceRequest = 0;
  let briefMode = 'create';
  let toastTimeout;
  let favorites = [];
  let theme;
  try { favorites = JSON.parse(localStorage.getItem('component-studio-saved') || '[]'); theme = localStorage.getItem('component-studio-theme'); } catch (_) {}
  if (!Array.isArray(favorites)) favorites = [];
  theme = theme === 'light' || theme === 'dark' ? theme : matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  const icons = () => { if (window.lucide) lucide.createIcons({attrs:{width:17,height:17}}); };
  const escape = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const selected = () => library.components.find(c => c.id === selectedId);
  const revision = () => { const c = selected(); return c && (c.versions.find(v => v.id === versionId) || c.versions[c.versions.length-1]); };
  const query = () => new URLSearchParams({component:selectedId,version:revision().id});
  const categoryIcon = name => ({Navigation:'panel-top',Inputs:'text-cursor-input',Feedback:'bell',Layout:'panels-top-left',Media:'image',Data:'chart-no-axes-combined',Components:'component'}[name] || 'shapes');

  function toast(message) {
    clearTimeout(toastTimeout);
    $('#toast span').textContent = message;
    $('#toast').hidden = false;
    toastTimeout = setTimeout(() => $('#toast').hidden = true, 2600);
  }

  function renderCategories() {
    const names = Array.from(new Set(library.components.map(c => c.category))).sort();
    const choices = [{id:'all',label:'All components',icon:'grid-2x2',count:library.components.length},{id:'saved',label:'Saved',icon:'bookmark',count:library.components.filter(c => favorites.includes(c.id)).length},...names.map(name => ({id:name,label:name,icon:categoryIcon(name),count:library.components.filter(c=>c.category===name).length}))];
    $('#categories').innerHTML = choices.map(c=>`<button class="category-button" type="button" data-category="${escape(c.id)}" aria-pressed="${category===c.id}"><i data-lucide="${c.icon}" aria-hidden="true"></i><span>${escape(c.label)}</span><span class="category-count">${c.count}</span></button>`).join('');
    $('#library-count').textContent = library.components.length;
    icons();
  }

  function renderList() {
    const term = $('#search').value.trim().toLowerCase();
    const entries = library.components.filter(c => (category==='all'||category==='saved'&&favorites.includes(c.id)||c.category===category) && `${c.name} ${c.description} ${c.category}`.toLowerCase().includes(term));
    $('#component-list').innerHTML = entries.map(c=>`<button class="component-card" type="button" data-component="${escape(c.id)}" aria-pressed="${c.id===selectedId}"><span class="component-card-icon"><i data-lucide="${categoryIcon(c.category)}" aria-hidden="true"></i></span><span class="component-card-title">${escape(c.name)}</span><span class="component-card-meta"><span>${escape(c.category)}</span><span>${c.versions.length} ${c.versions.length===1?'version':'versions'}</span></span></button>`).join('');
    $('#no-results').hidden = entries.length>0;
    icons();
  }

  async function loadCode() {
    const request = ++sourceRequest;
    const params = query(); params.set('file',sourceFile);
    try {
      const response = await fetch(`/api/source?${params}`);
      if(!response.ok) throw new Error('Could not load source');
      const file = await response.json();
      if(request!==sourceRequest) return;
      currentSource = file.content;
      $('#source-code').textContent = currentSource;
    } catch(error) { if(request===sourceRequest) $('#source-code').textContent=error.message; }
  }

  function renderDetail(forcePreview=false) {
    const component = selected();
    if(!component) return;
    const version = revision(); versionId = version.id;
    $('#selected-name').textContent = component.name;
    $('#selected-category').textContent = component.category;
    $('#selected-description').textContent = component.description;
    $('#favorite').setAttribute('aria-pressed',String(favorites.includes(component.id)));
    $('#favorite').setAttribute('aria-label',favorites.includes(component.id)?'Unsave component':'Save component');
    const selector = $('#version-select');
    selector.innerHTML = component.versions.slice().reverse().map(v=>`<option value="${escape(v.id)}">Version ${v.number} · ${escape(v.label)}</option>`).join('');
    selector.value = versionId;
    selector.hidden = component.versions.length<2;
    $('#one-version').hidden = component.versions.length>1;
    $('#one-version').textContent = `Version ${version.number} · ${version.label}`;
    if(!version.files.some(f=>f.name===sourceFile)) sourceFile = version.files[0].name;
    $('#source-files').innerHTML=version.files.map(f=>`<option value="${escape(f.name)}">${escape(f.name)}</option>`).join('');
    $('#source-files').value=sourceFile;
    $('#export').href=`/api/export?${query()}`;
    const nextKey = `${version.preview}|${theme}`;
    if(nextKey!==previewKey||forcePreview) {
      previewKey=nextKey;
      $('#component-preview').src=`/${version.preview}?theme=${theme}&reset=${forcePreview?Date.now():version.fingerprint.slice(0,8)}`;
    }
    $('#component-preview').title=`${component.name}, version ${version.number}, interactive preview`;
    $('#preview-device').style.width=width==='fit'?'100%':`${width}px`;
    $('#preview-stage').hidden=view!=='preview';$('#code-stage').hidden=view!=='code';
    document.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===view)));
    if(view==='code') loadCode();
    icons();
  }

  async function refresh() {
    try {
      const response = await fetch('/api/library');
      if(!response.ok) throw new Error('Could not load the collection');
      const next = await response.json();
      const mark = JSON.stringify(next);
      if(mark===fingerprint) return;
      const old = revision();
      library = next;fingerprint=mark;
      if(!selected()) selectedId=library.components[0]?.id;
      if(!selectedId) {$('#selected-name').textContent='Your first component';$('#selected-description').textContent='Create a component with Codex to start your collection.';return;}
      const component = selected();
      if(!old || !component.versions.some(v=>v.id===versionId) || old.id===component.versions.at(-2)?.id) versionId=component.versions.at(-1).id;
      renderCategories();renderList();renderDetail();
    } catch(error) { if(!library.components.length) $('#selected-name').textContent=error.message; }
  }

  function applyTheme() {
    document.documentElement.dataset.theme=theme;
    $('#theme-toggle').innerHTML=`<i data-lucide="${theme==='dark'?'sun':'moon'}" aria-hidden="true"></i>`;
    $('#theme-toggle').setAttribute('aria-label',`Switch to ${theme==='dark'?'light':'dark'} mode`);
    try { localStorage.setItem('component-studio-theme',theme); } catch(_) {}
    if(selected()) renderDetail();
    icons();
  }

  function openBrief(mode) {
    briefMode=mode;
    $('#brief-title').textContent=mode==='refine'?`Refine ${selected().name}`:'What are we making?';
    $('#brief').value='';
    $('#brief').placeholder=mode==='refine'?'Make the transitions a little softer, and add a compact version…':'A date picker that opens like a little stack of cards…';
    $('#prompt-preview').hidden=true;
    $('#brief-dialog').showModal();
  }

  async function copy(value, message) {
    try { await navigator.clipboard.writeText(value); toast(message); return true; }
    catch(_) {
      const helper=document.createElement('textarea');
      helper.value=value;helper.readOnly=true;
      helper.style.position='fixed';helper.style.left='-9999px';
      const container=$('#brief-dialog').open?$('#brief-dialog'):document.body;
      container.appendChild(helper);helper.select();
      let copied=false;
      try { copied=document.execCommand('copy'); } catch(_) {}
      helper.remove();
      if(copied)toast(message);
      return copied;
    }
  }

  $('#categories').addEventListener('click',event=>{const button=event.target.closest('[data-category]');if(button){category=button.dataset.category;renderCategories();renderList();}});
  $('#component-list').addEventListener('click',event=>{const button=event.target.closest('[data-component]');if(button){selectedId=button.dataset.component;versionId=null;sourceFile='source.html';const url=new URL(location);url.searchParams.set('component',selectedId);history.replaceState(null,'',url);renderList();renderDetail();}});
  $('#search').addEventListener('input',renderList);
  $('#favorite').addEventListener('click',()=>{if(!selectedId)return;favorites=favorites.includes(selectedId)?favorites.filter(id=>id!==selectedId):[...favorites,selectedId];try{localStorage.setItem('component-studio-saved',JSON.stringify(favorites));}catch(_){}renderCategories();renderList();renderDetail();});
  document.querySelectorAll('[data-view]').forEach(button=>button.addEventListener('click',()=>{view=button.dataset.view;renderDetail();}));
  document.querySelectorAll('[data-width]').forEach(button=>button.addEventListener('click',()=>{width=button.dataset.width;document.querySelectorAll('[data-width]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));renderDetail();}));
  $('#version-select').addEventListener('change',event=>{versionId=event.target.value;sourceFile='source.html';renderDetail();});
  $('#source-files').addEventListener('change',event=>{sourceFile=event.target.value;loadCode();});
  $('#reset-preview').addEventListener('click',()=>renderDetail(true));
  $('#theme-toggle').addEventListener('click',()=>{theme=theme==='light'?'dark':'light';applyTheme();});
  $('#copy-code').addEventListener('click',async()=>{if(!await copy(currentSource,'Code copied'))toast('Select the code and copy it.');});
  document.querySelectorAll('[data-new]').forEach(button=>button.addEventListener('click',()=>openBrief('create')));
  $('#refine').addEventListener('click',()=>{if(selected())openBrief('refine');});
  $('[data-close]').addEventListener('click',()=>$('#brief-dialog').close());
  $('#brief-dialog').addEventListener('click',event=>{if(event.target!==$('#brief-dialog'))return;const r=event.target.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)event.target.close();});
  $('#copy-prompt').addEventListener('click',async()=>{
    const brief=$('#brief').value.trim();
    if(!brief){$('#brief').focus();return;}
    const target=briefMode==='refine'?`Refine the existing component "${selected().name}" (id: ${selectedId}), starting from ${revision().id}. Preserve its history and save a new revision.`:'Create a new component and add it to my collection.';
    const prompt=`Use $component-studio.\n\nStudio: ${config.root}\n${target}\n\n${brief}\n\nKeep the preview in the gallery rather than inline in this chat. Save the finished component and verify its main interactions.`;
    $('#generated-prompt').value=prompt;
    $('#prompt-preview').hidden=false;
    if(await copy(prompt,'Prompt copied — paste it into a fresh Codex chat.'))$('#brief-dialog').close();
    else {$('#generated-prompt').focus();$('#generated-prompt').select();}
  });
  fetch('/api/health').then(response=>response.json()).then(health=>{config.root=health.root;}).catch(()=>{});
  applyTheme();refresh();
  setInterval(()=>{if(!document.hidden)refresh();},2500);
  document.addEventListener('visibilitychange',()=>{if(!document.hidden)refresh();});
})();
