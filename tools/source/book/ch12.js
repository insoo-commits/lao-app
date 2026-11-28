const fs=require('fs');const D=require('docx');
const {Header,PositionalTab,PositionalTabAlignment,PositionalTabRelativeTo,PositionalTabLeader,Document,Packer,Paragraph,TextRun,Table,TableRow,TableCell,WidthType,ShadingType,AlignmentType,HeadingLevel,LevelFormat,BorderStyle,PageBreak,Footer,PageNumber,TableLayoutType,VerticalAlign}=D;
const B=require('./ch12.json');const OUT=process.argv[2];
const KO='Malgun Gothic',LO='Leelawadee UI';
const isLao=c=>/[຀-໿]/.test(c);
function runs(t,o={}){const out=[];let cur='',lao=null;
  const push=()=>{if(!cur)return;const sz=(o.size||21)+(lao?3:0);out.push(new TextRun({text:cur,bold:o.bold,italics:o.it,color:o.color,size:sz,font:lao?{ascii:LO,hAnsi:LO,cs:LO,eastAsia:LO}:{ascii:KO,hAnsi:KO,eastAsia:KO,cs:KO}}));cur=''};
  for(const ch of String(t)){const l=isLao(ch)||(lao&&/[\s?!.,~—()]/.test(ch)&&false);const L=isLao(ch)?true:(/[\s]/.test(ch)?lao:false);if(L!==lao&&cur){push()}lao=L;cur+=ch}push();return out}
const P=(t,o={})=>new Paragraph({children:runs(t,o),spacing:{after:o.after??80,before:o.before??0,line:o.line??300},alignment:o.align,shading:o.shade?{type:ShadingType.CLEAR,fill:o.shade,color:'auto'}:undefined,border:o.border,indent:o.indent,keepNext:o.keepNext,numbering:o.num});
const H1=t=>new Paragraph({heading:HeadingLevel.HEADING_1,children:runs(t,{size:36,bold:true,color:'7A4E0E'})});
const H2=t=>new Paragraph({heading:HeadingLevel.HEADING_2,children:runs(t,{size:28,bold:true,color:'7A4E0E'}),border:{bottom:{style:BorderStyle.SINGLE,size:8,color:'C8A46A',space:4}}});
const H3=t=>new Paragraph({heading:HeadingLevel.HEADING_3,children:runs(t,{size:23,bold:true,color:'333333'})});
const W=9638;const bd={style:BorderStyle.SINGLE,size:4,color:'BFAF95'};const borders={top:bd,bottom:bd,left:bd,right:bd};
function table(widths,rows,{head=true,heights}={}){return new Table({width:{size:W,type:WidthType.DXA},columnWidths:widths,layout:TableLayoutType.FIXED,
  rows:rows.map((r,i)=>new TableRow({tableHeader:head&&i===0,cantSplit:true,height:heights?{value:heights,rule:'atLeast'}:undefined,children:r.map((c,j)=>new TableCell({width:{size:widths[j],type:WidthType.DXA},borders,verticalAlign:VerticalAlign.CENTER,
    shading:head&&i===0?{type:ShadingType.CLEAR,fill:'EFE3CC',color:'auto'}:undefined,margins:{top:50,bottom:50,left:90,right:90},
    children:[new Paragraph({spacing:{after:0,line:276},alignment:head&&i===0?AlignmentType.CENTER:undefined,children:runs(c,{size:head&&i===0?19:20,bold:head&&i===0})})]}))}))})}
const appBox=t=>P(t,{shade:'F3EEE4',size:19,color:'5A4A30',before:60,after:120,border:{left:{style:BorderStyle.SINGLE,size:18,color:'9A6A1E',space:6}}});
const bullet=(t,o={})=>P(t,{num:{reference:'b',level:0},after:40,...o});
const numb=(t,ref,o={})=>P(t,{num:{reference:ref,level:0},after:50,...o});
const note=w=>w[1].split(' · ').slice(1).join(' · ');
const codes=Object.keys(B);const kids=[];const ans=[];let qn=0;
// ---- chapter opening
kids.push(P('3부 장면 회화',{size:20,color:'8A7A60',after:40}));
kids.push(H1('12장  인사·기본 표현'));
kids.push(P('라오스 사람을 처음 만나서 인사하고, 내 소개를 하고, 네·아니요로 대답하고, 못 알아들었을 때 다시 물어보는 말을 배워요. 이 장의 말만 알아도 첫 만남을 끝까지 라오스어로 이어 갈 수 있어요.',{after:160}));
kids.push(H3('학습 목표'));
['ສະບາຍດີ, ຂອບໃຈ, ຂໍໂທດ 같은 기본 인사를 상황에 맞게 말할 수 있어요.','이름, 나라, 하는 일을 넣어 짧게 자기소개를 할 수 있어요.','ແມ່ນ·ໄດ້·ມີ와 ບໍ່로 대답하고, ບໍ? 로 물어볼 수 있어요.','모를 때 ‘천천히 말해 주세요’, ‘한 번 더’라고 부탁할 수 있어요.'].forEach(t=>kids.push(bullet(t)));
kids.push(H3('이 장의 앱 묶음'));
kids.push(P('앱에서 기초회화 → 인사·기본 표현을 누르면 아래 묶음이 차례로 나와요.',{size:19,after:80}));
kids.push(table([900,1500,4338,1450,1450],[['절','앱 코드','묶음','단어','대화'],...codes.map((k,i)=>['12-'+(i+1),k,B[k].t,B[k].w.length+'개',B[k].dl.length?B[k].dl.length+'줄':'—'])]));
kids.push(H3('공부 순서 (한 절에 30~40분)'));
[['책으로 읽기','단어 표와 풀이를 읽고 알아 두기를 확인해요.'],['앱으로 듣기','문장 탭에서 묶음 재생. 반복 2회, 속도 0.8로 시작해요.'],['책으로 쓰기','따라 쓰기와 듣고 받아쓰기를 해요.'],['앱으로 확인','퀴즈 탭을 풀고, 맞으면 완료 표시. 틀린 단어는 앱 복습 목록에 모여요.'],['역할극','짧은 대화를 앱과 번갈아 한 사람씩 말해 봐요.']].forEach(([a,b])=>kids.push(numb(a+': '+b,'steps')));
// ---- sections
codes.forEach((k,si)=>{const b=B[k];const sec='12-'+(si+1);
  kids.push(new Paragraph({children:[new PageBreak()]}));
  kids.push(H2(sec+'  '+b.t));
  kids.push(appBox('앱  기초회화 › 인사·기본 표현 › ['+k.slice(-2)+'] '+b.t+'   (묶음 코드 '+k+')'));
  kids.push(P(b.i,{after:120}));
  kids.push(H3('핵심 단어'));
  kids.push(table([640,2440,1730,2080,2748],[['번호','라오스어','독음','뜻','풀이'],...b.w.map((w,i)=>[String(i+1),w[0],w[2],w[3],note(w)])]));
  kids.push(H3('대표 예문'));
  kids.push(P('앱 단어 카드에는 단어마다 예문이 3개씩 있어요. 책에는 첫 번째 예문만 실었어요.',{size:18,color:'7A6A50',after:60}));
  kids.push(table([640,3560,2560,2878],[['번호','라오스어','독음','뜻'],...b.w.map((w,i)=>[String(i+1),w[4][0][0],w[4][0][1],w[4][0][2]])]));
  if(b.dl.length){kids.push(H3('짧은 대화'));
    kids.push(P('앱에서 첫째·셋째 줄은 여자 목소리, 둘째·넷째 줄은 남자 목소리로 나와요.',{size:18,color:'7A6A50',after:60}));
    kids.push(table([900,3300,2500,2938],[['사람','라오스어','독음','뜻'],...b.dl.map(d=>[d[0],d[1],d[2],d[3]])]))}
  kids.push(H3('알아 두기'));
  b.tp.forEach(t=>kids.push(bullet(t.replace(/^•\s*/,''))));
  if(b.sm&&b.sm.length){kids.push(H3('한 문장으로 정리'));kids.push(P(b.sm[0],{size:22,after:20}));kids.push(P(b.sm[1]+'  ·  '+b.sm[2],{size:19,color:'5A4A30',after:120}))}
  // practice
  kids.push(H3('연습 1  따라 쓰기'));
  const fw=b.w.slice(0,4);
  kids.push(table([2700,2312,2313,2313],[['보고 쓰기','','',''],...fw.map(w=>[w[0],' ',' ',' '])],{heights:620}));
  kids.push(H3('연습 2  듣고 받아쓰기 (앱)'));
  kids.push(P('앱 단어 탭에서 해당 단어 카드를 열고 두 번째 예문을 들어요. 듣고 라오 문자로 쓰세요. 뜻은 힌트예요.',{size:19,after:60}));
  const dw=b.w.slice(0,3);
  kids.push(table([640,3200,5798],[['번호','힌트 (뜻)','받아쓰기'],...dw.map((w,i)=>{const e=w[4][1];ans.push([sec+' 연습 2-'+(i+1),e[0]+'  ('+e[1]+')']);return [String(i+1),e[2]+'  [단어 '+(b.w.indexOf(w)+1)+' 예문 2]',' ']})],{heights:620}));
  kids.push(H3('연습 3  확인 문제'));
  b.qz.forEach((q,i)=>{kids.push(P((i+1)+'. '+q[0],{after:20}));kids.push(P('답: ______________________________',{color:'9A8A70',after:80,indent:{left:300}}));ans.push([sec+' 연습 3-'+(i+1),q[1]])});
  kids.push(appBox('앱 확인  이 묶음의 퀴즈 탭을 풀고, 다 맞으면 완료 표시를 눌러요. 틀린 단어는 다음 날 복습 목록에서 다시 봐요.'));
});
// ---- chapter end
kids.push(new Paragraph({children:[new PageBreak()]}));
kids.push(H2('12장 마무리'));
kids.push(H3('역할극: 처음 만난 날'));
kids.push(P('앞에서 배운 대화를 이어 붙인 장면이에요. 앱 듣기연습 ‘처음 만난 사람과 인사’(8-04-01)를 먼저 듣고, 빈칸을 채워 말해 보세요.',{after:80}));
kids.push(table([900,4300,4438],[['사람','라오스어','뜻'],['A','ສະບາຍດີ ____________?','안녕하세요, 잘 지내요?'],['B','ສະບາຍດີ ຂ້ອຍຊື່ ____________','안녕하세요, 저는 ○○이에요.'],['A','ເຈົ້າມາຈາກ____________?','어디에서 왔어요?'],['B','ຂ້ອຍມາຈາກ____________','저는 한국에서 왔어요.'],['A','ຂໍໂທດ ____________ແດ່','미안해요, 천천히 말해 주세요.'],['B','____________ ແລ້ວພົບກັນໃໝ່ເດີ້','만나서 반가워요. 또 만나요.']],{heights:560}));
kids.push(H3('점검표'));
kids.push(table([900,3938,1600,1600,1600],[['절','묶음','책 연습','앱 퀴즈','완료 표시'],...codes.map((k,i)=>['12-'+(i+1),B[k].t,'☐','☐','☐'])]));
kids.push(H3('더 해 보기 (앱)'));
[['8-04-01','듣기연습: 처음 만난 사람과 인사'],['4-01-01~03','짝말비교: ‘나’·‘너’·‘그’ 높낮이'],['4-06-07','짝말비교: 인사 높낮이 총정리'],['5-01-03~04','비슷한말: 의문사']].forEach(([c,t])=>kids.push(bullet(c+'  '+t)));
kids.push(new Paragraph({children:[new PageBreak()]}));
kids.push(H2('정답'));
kids.push(table([2200,7438],[['문제','답'],...ans]));
const doc=new Document({creator:'RYU',title:'12장 인사·기본 표현',
  styles:{default:{document:{run:{font:KO,size:21}}},
    paragraphStyles:[{id:'Heading1',name:'Heading 1',basedOn:'Normal',next:'Normal',quickFormat:true,run:{font:KO,size:36,bold:true},paragraph:{spacing:{before:0,after:160},keepNext:true,outlineLevel:0}},
      {id:'Heading2',name:'Heading 2',basedOn:'Normal',next:'Normal',quickFormat:true,run:{font:KO,size:28,bold:true},paragraph:{spacing:{before:0,after:120},keepNext:true,outlineLevel:1}},
      {id:'Heading3',name:'Heading 3',basedOn:'Normal',next:'Normal',quickFormat:true,run:{font:KO,size:23,bold:true},paragraph:{spacing:{before:220,after:80},keepNext:true,outlineLevel:2}}]},
  numbering:{config:[{reference:'b',levels:[{level:0,format:LevelFormat.BULLET,text:'•',alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:360,hanging:240}}}}]},
    {reference:'steps',levels:[{level:0,format:LevelFormat.DECIMAL,text:'%1.',alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:360,hanging:300}}}}]}]},
  sections:[{properties:{page:{margin:{top:1134,bottom:1134,left:1134,right:1134,header:567,footer:567}}},
    headers:{default:new Header({children:[new Paragraph({tabStops:[{type:D.TabStopType.RIGHT,position:9638}],spacing:{after:0},border:{bottom:{style:BorderStyle.SINGLE,size:6,color:'C8A46A',space:4}},children:[
      new TextRun({text:'ຮຽນ ພາສາລາວ',font:{ascii:LO,hAnsi:LO,cs:LO,eastAsia:LO},size:18,bold:true,color:'1F5E8C'}),
      new TextRun({text:'  라오스어 묶어서 공부하기  ·  3부 장면 회화',font:KO,size:16,color:'8A7A60'}),
      new TextRun({children:['\t','12장  인사·기본 표현'],font:KO,size:17,bold:true,color:'7A4E0E'})]})]})},
    footers:{default:new Footer({children:[new Paragraph({tabStops:[{type:D.TabStopType.RIGHT,position:9638}],spacing:{before:0,after:0},border:{top:{style:BorderStyle.SINGLE,size:4,color:'E2D6BF',space:4}},children:[
      new TextRun({text:'앱 기초회화 › 인사·기본 표현  (묶음 1-01-01 ~ 1-01-07)',font:KO,size:15,color:'9A8A70'}),
      new TextRun({children:['\t','12 – ',PageNumber.CURRENT],font:KO,size:18,bold:true,color:'7A4E0E'})]})]})},
    children:kids}]});
Packer.toBuffer(doc).then(b=>{fs.writeFileSync(OUT,b);console.log('ok',b.length)});
