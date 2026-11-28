const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:794,height:1123},deviceScaleFactor:2.5});
await p.goto('file://'+__dirname+'/poster.html');await p.waitForLoadState('networkidle');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(600);
console.log(await p.evaluate(()=>{const r=e=>Math.round(document.querySelector(e).getBoundingClientRect().bottom);return {cards:[...document.querySelectorAll('.card')].map(c=>Math.round(c.getBoundingClientRect().bottom)),tip:r('.tip'),foot:r('.foot'),lao:document.fonts.check('12px "Noto Sans Lao Looped"')}}));
await p.pdf({path:'poster.pdf',format:'A4',printBackground:true,margin:{top:0,right:0,bottom:0,left:0}});
await p.locator('.page').screenshot({path:'poster.png'});await b.close()})();
