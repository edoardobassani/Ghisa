"""Aiuto per i test a passi (u7, u8): ogni passo riceve `u` con tocchi per testo, valutazioni e schermate.
run([('nome', passo), ...]) esegue i passi in ordine sulla stessa pagina e stampa il risultato di ognuno."""
import gb
from playwright.async_api import async_playwright


class U:
    def __init__(self, pg):
        self.pg = pg

    async def ev(self, js):
        r = await self.pg.evaluate(js)
        await self.pg.wait_for_timeout(120)
        return r

    async def tap(self, text, exact=False):
        loc = self.pg.get_by_role('button', name=text, exact=exact).first
        await loc.click()
        await self.pg.wait_for_timeout(200)

    async def fill(self, sel, v):
        await self.pg.fill(sel, v)

    async def text(self):
        return await self.pg.evaluate("()=>document.querySelector('#v').innerText")

    async def toast(self):
        return await self.pg.evaluate("()=>{const t=document.querySelector('#undo,#toast,.toast');return t?t.innerText:''}")

    async def shot(self, name):
        await self.pg.screenshot(path=gb.O + name + '.png')


async def _run(steps):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 390, 'height': 844})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(gb.URL)
        await pg.wait_for_timeout(600)
        u = U(pg)
        for name, f in steps:
            print(name + ':', await f(u))
        print('errori:', errs)
        await b.close()


def run(steps):
    return _run(steps)
