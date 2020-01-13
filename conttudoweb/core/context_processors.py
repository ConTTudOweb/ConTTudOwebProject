EMPRESA_NAME = "ConTTudOweb"
EMPRESA_SLOGAN = "Soluções em tecnologia"
EMPRESA_DESCRIPTION = "A " + EMPRESA_NAME + " é uma empresa de tecnologia dedicada a entregar produtos de qualidade e atualizados!"

KEYWORDS = \
    "conttudo web, conttudo, criar site, website, design, responsivo, marketing digital, ecommerce, e-commerce, " \
    "desenvolvimento, desenvolvimento site, desenvolvimento web, sites, apucarana, paraná, empresa de web, web, " \
    "criaçoes de sites, sistemas web, conttudo apucarana, manutenção de sites, banners, SEO, Lojas Virtuais, " \
    "wordpress, agencia web, Publicidade On Line, design web, sites responsivos, sites apucarana, " \
    "lojas virtuais apucarana, e-commerces apucarana, catalogo online, sistemas online"

PAGES = dict(
    PAGE_HOME={
        "title": EMPRESA_SLOGAN,
        "description": EMPRESA_DESCRIPTION,
        "keywords": "%s" % KEYWORDS
    }
)

def consts(request):
    return dict(
        EMPRESA={
            "name": EMPRESA_NAME,
            "slogan": EMPRESA_SLOGAN,
            "email": "contato@conttudoweb.com.br"
        }
    )
