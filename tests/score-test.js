// node tests/score-test.js  — fails if scoring or matching breaks
const fs=require('fs'),assert=require('assert');
const h=fs.readFileSync(__dirname+'/../index.html','utf8');
let js=h.split('<script>')[1].split('</script>')[0].replace("'use strict';",'').replace(/\nrender\(\);\s*$/,'\n');
const store={};global.localStorage={getItem:k=>k in store?store[k]:null,setItem:(k,v)=>{store[k]=v}};
global.document={getElementById:()=>null,querySelector:()=>null,addEventListener:()=>{},createElement:()=>({})};
global.window={scrollTo(){}};global.confirm=()=>true;
const fn=new Function(js+'\nreturn {S,results,matches,SECTIONS,TOTAL_Q,JOBS,IP_ITEMS,BF_ITEMS,MB_ITEMS,DI_ITEMS,EN_ITEMS,A};');
const X=fn();
assert.strictEqual(X.TOTAL_Q,177);assert.strictEqual(X.JOBS.length,923);assert.strictEqual(X.IP_ITEMS.length,60);
assert.strictEqual(X.results(),null,'no result before answers');
const S=X.S;
S.answers.ip=Array.from({length:60},(_,i)=>[2,5,4,3,5,1][Math.floor(i/10)]);
S.answers.bf=Array.from({length:50},()=>5);
S.answers.mb=[5,4,5,4,5, 4,5,5,4,5, 2,1,2,2,1, 4,5,4,5,5];
S.answers.di=[5,4,5,4,5, 4,4,5,5,5, 2,2,3,1,2, 3,4,2,3,4];
S.answers.en=[3,4,3, 3,3,2, 5,4,5, 2,3,2, 3,3,2, 2,3,2, 5,5,5, 4,5,5, 2,2,2];
const R=X.results();
assert.strictEqual(R.mb.type,'INTP');assert.strictEqual(R.holland,'IEA');assert.strictEqual(R.di.code,'Di');
assert.strictEqual(R.en.type,7);assert.strictEqual(R.en.wing,8);
// all-5 on IPIP: + keyed items max, - keyed items reverse to 1 → extraversion = (5*5+1*5 -10)/40 = 50%
assert.strictEqual(R.bf[0],50);
S.answers.bf=X.BF_ITEMS.map(it=>it.k>0?5:1);assert.deepStrictEqual(X.results().bf,[100,100,100,100,100]);
S.answers.bf=X.BF_ITEMS.map(it=>it.k>0?1:5);assert.deepStrictEqual(X.results().bf,[0,0,0,0,0]);
const m=X.matches(R.ip);assert.ok(m[0].m>m[m.length-1].m);assert.ok(m.every(x=>x.m>=0&&x.m<=100));
assert.ok(m.slice(0,20).some(x=>/Scientist|Analyst|Research/.test(x.j.t)),'an I-E-A profile should rank investigative work high');
// a Realistic-only profile ranks trades, not scientists
const r=X.matches([40,0,0,0,0,0]);assert.strictEqual(r[0].j.i.indexOf(Math.max(...r[0].j.i)),0,r[0].j.t+' should be Realistic-led');
// resume lands on the first unanswered question
S.answers.ip[7]=null;X.A.quiz();assert.strictEqual(S.sec,0);assert.strictEqual(S.qi,7);
console.log('score-test: all green');
