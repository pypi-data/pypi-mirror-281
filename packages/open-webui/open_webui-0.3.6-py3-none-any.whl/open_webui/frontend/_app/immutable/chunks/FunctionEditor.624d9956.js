import{s as De,p as te,f as r,a as P,l as me,g as d,h as x,R as ae,c as q,m as he,d as m,j as a,i as ie,r as l,Q as U,u as G,O as Te,n as pe,W as ge,v as Ce,V as Ve,P as Me,w as Fe,C as He}from"./scheduler.8ceb707f.js";import{S as Pe,i as qe,f as ve,b as _e,d as ye,m as be,a as we,t as xe,e as Ie}from"./index.07e72a31.js";import{g as Ae}from"./navigation.cffc86d9.js";import{C as Le}from"./CodeEditor.6552970f.js";import{C as Ne}from"./ConfirmDialog.070934a0.js";function Oe(t){let i,s=`<div class="bg-yellow-500/20 text-yellow-700 dark:text-yellow-200 rounded-lg px-4 py-3"><div>Please carefully review the following warnings:</div> <ul class="mt-1 list-disc pl-4 text-xs"><li>Functions allow arbitrary code execution.</li> <li>Do not install functions from sources you do not fully trust.</li></ul></div> <div class="my-3">I acknowledge that I have read and I understand the implications of my action. I am aware of
			the risks associated with executing arbitrary code and I have verified the trustworthiness of
			the source.</div>`;return{c(){i=r("div"),i.innerHTML=s,this.h()},l(o){i=d(o,"DIV",{class:!0,"data-svelte-h":!0}),ae(i)!=="svelte-1pkea5f"&&(i.innerHTML=s),this.h()},h(){a(i,"class","text-sm text-gray-500")},m(o,k){ie(o,i,k)},p:He,d(o){o&&m(i)}}}function Be(t){let i,s,o,k,p,g,A='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-4 h-4"><path fill-rule="evenodd" d="M17 10a.75.75 0 01-.75.75H5.612l4.158 3.96a.75.75 0 11-1.04 1.08l-5.5-5.25a.75.75 0 010-1.08l5.5-5.25a.75.75 0 111.04 1.08L5.612 9.25H16.25A.75.75 0 0117 10z" clip-rule="evenodd"></path></svg>',C,I,w=t[8].t("Back")+"",v,V,f,h,E,_,L,c,S,y,j,F,b,z,W,D,M,J=`<div class="text-xs text-gray-500 line-clamp-2"><span class="font-semibold dark:text-gray-200">Warning:</span> Functions allow
							arbitrary code execution <br/>—
							<span class="font-medium dark:text-gray-400">don&#39;t install random functions from sources you don&#39;t trust.</span></div>`,n,N,R=t[8].t("Save")+"",K,X,T,se,O,ne,le;function ke(e){t[17](e)}let oe={boilerplate:t[10]};t[3]!==void 0&&(oe.value=t[3]),b=new Le({props:oe}),te.push(()=>ve(b,"value",ke)),t[18](b),b.$on("save",t[19]);function Ee(e){t[22](e)}let re={$$slots:{default:[Oe]},$$scope:{ctx:t}};return t[6]!==void 0&&(re.show=t[6]),T=new Ne({props:re}),te.push(()=>ve(T,"show",Ee)),T.$on("confirm",t[23]),{c(){i=r("div"),s=r("div"),o=r("form"),k=r("div"),p=r("button"),g=r("div"),g.innerHTML=A,C=P(),I=r("div"),v=me(w),V=P(),f=r("div"),h=r("div"),E=r("div"),_=r("input"),L=P(),c=r("input"),S=P(),y=r("input"),j=P(),F=r("div"),_e(b.$$.fragment),W=P(),D=r("div"),M=r("div"),M.innerHTML=J,n=P(),N=r("button"),K=me(R),X=P(),_e(T.$$.fragment),this.h()},l(e){i=d(e,"DIV",{class:!0});var u=x(i);s=d(u,"DIV",{class:!0});var Q=x(s);o=d(Q,"FORM",{class:!0});var H=x(o);k=d(H,"DIV",{class:!0});var de=x(k);p=d(de,"BUTTON",{class:!0,type:!0});var Y=x(p);g=d(Y,"DIV",{class:!0,"data-svelte-h":!0}),ae(g)!=="svelte-1t52rj4"&&(g.innerHTML=A),C=q(Y),I=d(Y,"DIV",{class:!0});var ue=x(I);v=he(ue,w),ue.forEach(m),Y.forEach(m),de.forEach(m),V=q(H),f=d(H,"DIV",{class:!0});var B=x(f);h=d(B,"DIV",{class:!0});var Z=x(h);E=d(Z,"DIV",{class:!0});var $=x(E);_=d($,"INPUT",{class:!0,type:!0,placeholder:!0}),L=q($),c=d($,"INPUT",{class:!0,type:!0,placeholder:!0}),$.forEach(m),S=q(Z),y=d(Z,"INPUT",{class:!0,type:!0,placeholder:!0}),Z.forEach(m),j=q(B),F=d(B,"DIV",{class:!0});var fe=x(F);ye(b.$$.fragment,fe),fe.forEach(m),W=q(B),D=d(B,"DIV",{class:!0});var ee=x(D);M=d(ee,"DIV",{class:!0,"data-svelte-h":!0}),ae(M)!=="svelte-11344qq"&&(M.innerHTML=J),n=q(ee),N=d(ee,"BUTTON",{class:!0,type:!0});var ce=x(N);K=he(ce,R),ce.forEach(m),ee.forEach(m),B.forEach(m),H.forEach(m),Q.forEach(m),u.forEach(m),X=q(e),ye(T.$$.fragment,e),this.h()},h(){a(g,"class","self-center"),a(I,"class","self-center font-medium text-sm"),a(p,"class","flex space-x-1"),a(p,"type","button"),a(k,"class","mb-2.5"),a(_,"class","w-full px-3 py-2 text-sm font-medium bg-gray-50 dark:bg-gray-850 dark:text-gray-200 rounded-lg outline-none"),a(_,"type","text"),a(_,"placeholder","Function Name (e.g. My Filter)"),_.required=!0,a(c,"class","w-full px-3 py-2 text-sm font-medium disabled:text-gray-300 dark:disabled:text-gray-700 bg-gray-50 dark:bg-gray-850 dark:text-gray-200 rounded-lg outline-none"),a(c,"type","text"),a(c,"placeholder","Function ID (e.g. my_filter)"),c.required=!0,c.disabled=t[4],a(E,"class","flex gap-2 w-full"),a(y,"class","w-full px-3 py-2 text-sm font-medium bg-gray-50 dark:bg-gray-850 dark:text-gray-200 rounded-lg outline-none"),a(y,"type","text"),a(y,"placeholder","Function Description (e.g. A filter to remove profanity from text)"),y.required=!0,a(h,"class","w-full mb-2 flex flex-col gap-1.5"),a(F,"class","mb-2 flex-1 overflow-auto h-0 rounded-lg"),a(M,"class","flex-1 pr-3"),a(N,"class","px-3 py-1.5 text-sm font-medium bg-emerald-600 hover:bg-emerald-700 text-gray-50 transition rounded-lg"),a(N,"type","submit"),a(D,"class","pb-3 flex justify-between"),a(f,"class","flex flex-col flex-1 overflow-auto h-0 rounded-lg"),a(o,"class","flex flex-col max-h-[100dvh] h-full"),a(s,"class","mx-auto w-full md:px-0 h-full"),a(i,"class","flex flex-col justify-between w-full overflow-y-auto h-full")},m(e,u){ie(e,i,u),l(i,s),l(s,o),l(o,k),l(k,p),l(p,g),l(p,C),l(p,I),l(I,v),l(o,V),l(o,f),l(f,h),l(h,E),l(E,_),U(_,t[0]),l(E,L),l(E,c),U(c,t[1]),l(h,S),l(h,y),U(y,t[2].description),l(f,j),l(f,F),be(b,F,null),l(f,W),l(f,D),l(D,M),l(D,n),l(D,N),l(N,K),t[20](o),ie(e,X,u),be(T,e,u),O=!0,ne||(le=[G(p,"click",t[13]),G(_,"input",t[14]),G(c,"input",t[15]),G(y,"input",t[16]),G(o,"submit",Te(t[21]))],ne=!0)},p(e,[u]){(!O||u&256)&&w!==(w=e[8].t("Back")+"")&&pe(v,w),u&1&&_.value!==e[0]&&U(_,e[0]),(!O||u&16)&&(c.disabled=e[4]),u&2&&c.value!==e[1]&&U(c,e[1]),u&4&&y.value!==e[2].description&&U(y,e[2].description);const Q={};!z&&u&8&&(z=!0,Q.value=e[3],ge(()=>z=!1)),b.$set(Q),(!O||u&256)&&R!==(R=e[8].t("Save")+"")&&pe(K,R);const H={};u&268435456&&(H.$$scope={dirty:u,ctx:e}),!se&&u&64&&(se=!0,H.show=e[6],ge(()=>se=!1)),T.$set(H)},i(e){O||(we(b.$$.fragment,e),we(T.$$.fragment,e),O=!0)},o(e){xe(b.$$.fragment,e),xe(T.$$.fragment,e),O=!1},d(e){e&&(m(i),m(X)),t[18](null),Ie(b),t[20](null),Ie(T,e),ne=!1,Ce(le)}}}function Ue(t,i,s){let o;const k=Ve(),p=Me("i18n");Fe(t,p,n=>s(8,o=n));let g=null,A=!1,{edit:C=!1}=i,{clone:I=!1}=i,{id:w=""}=i,{name:v=""}=i,{meta:V={description:""}}=i,{content:f=""}=i,h,E=`from pydantic import BaseModel
from typing import Optional


class Filter:
    class Valves(BaseModel):
        max_turns: int = 4
        pass

    def __init__(self):
        # Indicates custom file handling logic. This flag helps disengage default routines in favor of custom
        # implementations, informing the WebUI to defer file-related operations to designated methods within this class.
        # Alternatively, you can remove the files directly from the body in from the inlet hook
        self.file_handler = True

        # Initialize 'valves' with specific configurations. Using 'Valves' instance helps encapsulate settings,
        # which ensures settings are managed cohesively and not confused with operational flags like 'file_handler'.
        self.valves = self.Valves(**{"max_turns": 2})
        pass

    def inlet(self, body: dict, user: Optional[dict] = None) -> dict:
        # Modify the request body or validate it before processing by the chat completion API.
        # This function is the pre-processor for the API where various checks on the input can be performed.
        # It can also modify the request before sending it to the API.
        print(f"inlet:{__name__}")
        print(f"inlet:body:{body}")
        print(f"inlet:user:{user}")

        if user.get("role", "admin") in ["user", "admin"]:
            messages = body.get("messages", [])
            if len(messages) > self.valves.max_turns:
                raise Exception(
                    f"Conversation turn limit exceeded. Max turns: {self.valves.max_turns}"
                )

        return body

    def outlet(self, body: dict, user: Optional[dict] = None) -> dict:
        # Modify or analyze the response body after processing by the API.
        # This function is the post-processor for the API, which can be used to modify the response
        # or perform additional checks and analytics.
        print(f"outlet:{__name__}")
        print(f"outlet:body:{body}")
        print(f"outlet:user:{user}")

        messages = [
            {
                **message,
                "content": f"{message['content']} - @@Modified from Filter Outlet",
            }
            for message in body.get("messages", [])
        ]

        return {"messages": messages}

`;const _=async()=>{k("save",{id:w,name:v,meta:V,content:f})},L=async()=>{h&&await h.formatPythonCodeHandler()&&(console.log("Code formatted successfully"),_())},c=()=>{Ae("/workspace/functions")};function S(){v=this.value,s(0,v)}function y(){w=this.value,s(1,w),s(0,v),s(4,C),s(12,I)}function j(){V.description=this.value,s(2,V)}function F(n){f=n,s(3,f)}function b(n){te[n?"unshift":"push"](()=>{h=n,s(7,h)})}const z=()=>{g&&g.requestSubmit()};function W(n){te[n?"unshift":"push"](()=>{g=n,s(5,g)})}const D=()=>{C?L():s(6,A=!0)};function M(n){A=n,s(6,A)}const J=()=>{L()};return t.$$set=n=>{"edit"in n&&s(4,C=n.edit),"clone"in n&&s(12,I=n.clone),"id"in n&&s(1,w=n.id),"name"in n&&s(0,v=n.name),"meta"in n&&s(2,V=n.meta),"content"in n&&s(3,f=n.content)},t.$$.update=()=>{t.$$.dirty&4113&&v&&!C&&!I&&s(1,w=v.replace(/\s+/g,"_").toLowerCase())},[v,w,V,f,C,g,A,h,o,p,E,L,I,c,S,y,j,F,b,z,W,D,M,J]}class Qe extends Pe{constructor(i){super(),qe(this,i,Ue,Be,De,{edit:4,clone:12,id:1,name:0,meta:2,content:3})}}export{Qe as F};
//# sourceMappingURL=FunctionEditor.624d9956.js.map
