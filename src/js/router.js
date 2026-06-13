/* KSC.JUSNREM — Constitutional Intelligence Engine · constitution.codes
   Hash router: shareable deep links for every view.
     #art-6            Article 6 (current era)
     #art-58@8         Article 58 as it stood after the 8th commit (Eighth Amendment era)
     #preamble         The Preamble
     #amdt-15          Constitutional history, card 15 open (Eighteenth Amendment)
     #lin-goi1858      Lineage card (Government of India Act 1858)
     #ppc-302          Pakistan Penal Code s.302
     #crpc-497         Code of Criminal Procedure s.497
     #timeline #lineage #compare #search #about   plain views
   Loads after the main script and wraps its global functions, so the
   engine itself stays untouched. */
(function(){
  "use strict";
  const C = window.CONSTITUTION_DATA, S = window.STATUTES || [];
  const numKey = {};
  for(const k in C.articles) numKey[String(C.articles[k].num).toLowerCase()] = k;
  let applying = false, ready = false;

  function currentHash(){
    switch(state.view){
      case "browse": {
        const a = C.articles[state.article];
        let h = state.article === "preamble" ? "preamble" : "art-" + a.num;
        if(state.era < C.commits.length - 1) h += "@" + state.era;
        return h;
      }
      case "statutes":
        return state.statute ? state.statute + (state.section ? "-" + state.section : "") : "statutes";
      case "timeline": case "lineage": case "compare": case "search": case "about": case "relay":
        return state.view;
    }
    return "";
  }
  function sync(){
    if(applying || !ready) return;
    const h = currentHash();
    if(h) history.replaceState(null, "", "#" + h);
  }

  // wrap the engine's navigation functions so every move updates the URL
  ["switchView","setEra","renderReader","renderSecReader","openTl","openLin"].forEach(fn=>{
    const orig = window[fn];
    if(typeof orig !== "function") return;
    window[fn] = function(){ const r = orig.apply(this, arguments); sync(); return r; };
  });

  function apply(){
    const h = decodeURIComponent(location.hash.slice(1));
    if(!h) return;
    applying = true;
    try{
      let m;
      if(h === "preamble"){
        state.article = "preamble"; setEra(state.era); switchView("browse");
      } else if((m = h.match(/^art-([0-9]+[A-Za-z]*)(?:@(\d+))?$/i))){
        const key = numKey[m[1].toLowerCase()];
        if(key){
          state.article = key;
          const era = m[2] !== undefined ? Math.min(+m[2], C.commits.length-1) : state.era;
          setEra(era); switchView("browse");
        }
      } else if((m = h.match(/^amdt-(\d+)$/))){
        const i = Math.min(+m[1], C.commits.length-1);
        switchView("timeline"); openTl(i);
      } else if((m = h.match(/^lin-(.+)$/))){
        openLin(m[1]);
      } else if(["timeline","lineage","compare","search","about","statutes","browse","home","relay"].indexOf(h) >= 0){
        switchView(h);
      } else if(h === "time-machine") {
        switchView("browse");
      } else if(h === "amendments") {
        switchView("timeline");
      } else {
        for(const st of S){
          const mm = h.match(new RegExp("^" + st.id + "-(.+)$"));
          if(mm && st.sections.some(x => x.num === mm[1])){ openSection(st.id, mm[1]); break; }
        }
      }
    } finally { applying = false; }
    ready = true; sync();
  }

  window.addEventListener("hashchange", apply);
  apply();          // honour a deep link on first load
  ready = true;
})();
