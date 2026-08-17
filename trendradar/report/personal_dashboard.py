"""Personalized presentation layer for the public intelligence report."""

from __future__ import annotations


PERSONAL_CSS = r"""
<style id="wisdom-signal-theme">
:root{--ink:#172033;--paper:#f4f7fb;--surface:#fff;--blue:#2f6df6;--teal:#168f91;--amber:#e6a238;--muted:#68748a;--line:#dce3ee}
*{box-sizing:border-box}body.personal-intel{margin:0;color:var(--ink);background:linear-gradient(90deg,var(--blue) 0 7px,transparent 7px),var(--paper);font-family:"Yu Gothic UI","Hiragino Sans","Noto Sans CJK SC","Microsoft YaHei UI",sans-serif}
body.personal-intel .reading-progress{height:3px;background:var(--blue)}body.personal-intel .container{max-width:1160px;margin:auto;background:transparent;box-shadow:none}
body.personal-intel .header{position:relative;margin:22px 18px 0;padding:30px 34px 24px;overflow:hidden;border:1px solid #26334d;border-radius:18px 18px 5px 5px;background:var(--ink)!important;box-shadow:0 18px 45px rgba(26,37,59,.12)}
body.personal-intel .header:after{content:"SIGNAL / TOKYO";position:absolute;right:28px;bottom:18px;color:rgba(255,255,255,.08);font:700 34px/1 "Bahnschrift Condensed","Arial Narrow",sans-serif;letter-spacing:.12em;pointer-events:none}
body.personal-intel .header-watermark{display:none}body.personal-intel .header-title{margin:0 0 22px;color:#fff;font-size:clamp(25px,4vw,42px);font-weight:720;letter-spacing:-.04em;text-align:left}
body.personal-intel .signal-eyebrow{display:block;margin-bottom:8px;color:#8facff;font:700 11px/1.2 "Bahnschrift","Arial Narrow",sans-serif;letter-spacing:.2em;text-transform:uppercase}
body.personal-intel .header-info{display:grid;grid-template-columns:repeat(4,minmax(100px,1fr));gap:8px 22px;max-width:760px}body.personal-intel .info-item{align-items:flex-start;text-align:left}body.personal-intel .info-item:nth-child(n+5){display:none}
body.personal-intel .info-label{color:#92a0bb;font-size:11px;letter-spacing:.05em}body.personal-intel .info-value{color:#fff;font:650 15px/1.5 "Bahnschrift","Yu Gothic UI",sans-serif}
body.personal-intel .save-buttons{top:26px;right:28px}body.personal-intel .toggle-wide-btn{display:none}body.personal-intel .toggle-dark-btn,body.personal-intel .save-btn,body.personal-intel .save-dropdown-trigger{border:1px solid rgba(255,255,255,.18);background:rgba(255,255,255,.07);box-shadow:none}
body.personal-intel .signal-admin{display:inline-flex;align-items:center;min-height:34px;padding:0 13px;border:1px solid rgba(255,255,255,.22);border-radius:8px;color:#fff;background:rgba(47,109,246,.28);font-size:12px;font-weight:650;text-decoration:none}body.personal-intel .signal-admin:hover{background:rgba(47,109,246,.48)}
body.personal-intel .signal-brief{position:relative;margin:14px 18px 0;padding:22px 26px 22px 31px;border:1px solid var(--line);border-radius:5px 5px 14px 14px;background:var(--surface)}body.personal-intel .signal-brief:before{content:"";position:absolute;left:0;top:20px;bottom:20px;width:4px;border-radius:0 4px 4px 0;background:var(--blue)}
body.personal-intel .signal-brief-kicker{margin-bottom:7px;color:var(--blue);font:700 11px/1.2 "Bahnschrift",sans-serif;letter-spacing:.16em}body.personal-intel .signal-brief h2{margin:0 0 6px;font-size:20px;letter-spacing:-.02em}body.personal-intel .signal-brief p{margin:0;color:var(--muted);font-size:13px;line-height:1.75}
body.personal-intel .content{margin:0 18px 24px;padding:24px 26px 34px;background:transparent}body.personal-intel .search-bar{margin:0 0 22px}body.personal-intel .search-input{height:43px;border:1px solid var(--line);border-radius:9px;background:rgba(255,255,255,.85);box-shadow:none}
body.personal-intel .rss-section,body.personal-intel .hotlist-section{margin:0 0 28px}body.personal-intel .rss-section-header{margin-bottom:12px;padding:0 0 9px;border-bottom:2px solid var(--ink)}body.personal-intel .rss-section-title{color:var(--ink);font-size:17px;font-weight:720}body.personal-intel .rss-section-count{color:var(--muted)}
body.personal-intel .rss-feeds-grid{display:grid;grid-template-columns:1fr;gap:10px}body.personal-intel .feed-group{padding:15px 17px;border:1px solid var(--line);border-radius:10px;background:var(--surface);box-shadow:none}body.personal-intel .feed-header{border-bottom-color:var(--line)}body.personal-intel .feed-name{color:var(--teal);font-weight:720}
body.personal-intel .rss-item{padding:11px 0;border-radius:0;background:transparent}body.personal-intel .rss-link{color:var(--ink);font-size:14px;line-height:1.55}
body.personal-intel .tab-bar-wrapper{margin:0 0 14px}body.personal-intel .tab-bar{gap:6px}body.personal-intel .tab-btn{border:1px solid var(--line);border-radius:999px;color:var(--muted);background:var(--surface)}body.personal-intel .tab-btn.active{color:#fff;border-color:var(--ink);background:var(--ink)}
body.personal-intel .word-group{position:relative;margin:0 0 12px;overflow:hidden;border:1px solid var(--line);border-radius:10px;background:var(--surface);box-shadow:none}body.personal-intel .word-group:before{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--blue)}
body.personal-intel .word-header{padding:15px 18px 13px 21px;background:#f9fbfe}body.personal-intel .word-name{color:var(--ink);font-size:16px;font-weight:720}body.personal-intel .word-count{color:var(--blue)!important}body.personal-intel .word-index{color:#8b96aa;font-family:"Bahnschrift",sans-serif}
body.personal-intel .news-item{margin:0;padding:13px 18px 13px 21px;border:0;border-top:1px solid #edf1f6;border-radius:0;background:transparent;box-shadow:none}body.personal-intel .news-item:hover{background:#f7f9fd;transform:none}body.personal-intel .news-number{color:#8590a4;background:#eef2f8}
body.personal-intel .news-link{color:var(--ink);font-size:14px;line-height:1.55}body.personal-intel .source-name{color:var(--teal)}body.personal-intel .rank-num.top{color:#9b6506;background:#fff2d6}body.personal-intel .section-divider{display:none}body.personal-intel .footer{color:var(--muted);background:transparent}body.personal-intel .fab-bar{opacity:.65}
@media(max-width:760px){body.personal-intel{background:var(--paper)}body.personal-intel .header{margin:0;padding:24px 20px 20px;border-radius:0 0 12px 12px}body.personal-intel .header:after{display:none}body.personal-intel .header-title{font-size:28px;margin-bottom:18px}body.personal-intel .header-info{grid-template-columns:repeat(2,minmax(0,1fr))}body.personal-intel .save-buttons{position:static;margin-top:18px;justify-content:flex-start}body.personal-intel .signal-brief{margin:10px 10px 0;padding:18px 18px 18px 23px}body.personal-intel .content{margin:0 10px 18px;padding:20px 0}}
@media(prefers-reduced-motion:reduce){body.personal-intel *,body.personal-intel *:before,body.personal-intel *:after{scroll-behavior:auto!important;transition:none!important;animation:none!important}}
</style>
"""


PERSONAL_JS = r"""
<script id="wisdom-signal-script">
document.addEventListener('DOMContentLoaded',function(){
document.body.classList.add('personal-intel');document.title='WISDOM SIGNAL · 个人情报台';
var title=document.querySelector('.header-title');if(title){title.textContent='今日情报信号';var eyebrow=document.createElement('span');eyebrow.className='signal-eyebrow';eyebrow.textContent='WISDOM SIGNAL / PERSONAL BRIEFING';title.prepend(eyebrow)}
var header=document.querySelector('.header');if(header&&!document.querySelector('.signal-brief')){var brief=document.createElement('section');brief.className='signal-brief';brief.innerHTML='<div class="signal-brief-kicker">FOCUS, NOT FEED</div><h2>只保留能影响工作判断的信息</h2><p>优先关注日本 IT 市场、制造业 AI、企业数据平台、云架构与模型工具链。社会热搜和重复事件不再占据第一屏。</p>';header.insertAdjacentElement('afterend',brief)}
var buttons=document.querySelector('.save-buttons');if(buttons&&!buttons.querySelector('.signal-admin')){var admin=document.createElement('a');admin.className='signal-admin';admin.href='http://127.0.0.1:8765/';admin.textContent='管理消息源';admin.title='电脑在线时打开本地管理后台';buttons.prepend(admin)}
document.querySelectorAll('.rss-section-title').forEach(function(el,i){el.textContent=i===0?'最新信号':'订阅来源'});var search=document.querySelector('.search-input');if(search)search.placeholder='搜索今天的有效信号…';
});
</script>
"""


def personalize_html(html: str) -> str:
    """Inject the personal report theme into a generated standalone page."""
    if "wisdom-signal-theme" in html:
        return html
    html = html.replace("</head>", f"{PERSONAL_CSS}\n</head>", 1) if "</head>" in html else PERSONAL_CSS + html
    html = html.replace("</body>", f"{PERSONAL_JS}\n</body>", 1) if "</body>" in html else html + PERSONAL_JS
    return html
