import json
import random
from itertools import combinations

# === Bases lexicales ===
prefixes = [
    "néo", "paléo", "archéo", "hyper", "trans", "meta", "post", "pré", "crypto", "neuro",
    "holo", "fracto", "tachyo", "entropo", "plasmo", "spectro", "glitch", "quant", "xeno",
    "noo", "psy", "thanato", "chton", "vortico", "phréa", "kaléido", "proto", "démiurgo",
    "eschat", "médio", "hypno", "cata", "entélé", "téléo", "axioma", "heurist", "stochast",
    "causo", "acauso", "chrono", "infundi", "tétradi", "topo", "géomé", "réso", "diffra",
    "interfé", "coher", "superpo", "entrela", "discret", "conti", "fuzzy", "crisp", "bayés",
    "markov", "récurs", "itéra", "lamina", "turbu", "granu", "crista", "amor", "nano",
    "méso", "macro", "cosmo", "subplanck", "supralumi", "sublumi", "gravito", "électro",
    "chromo", "super", "brana", "calabi", "orbifold", "conifold", "worm", "kerr", "schwarz",
    "minkowski", "eucli", "lorentz", "galilé", "newton", "semiclass", "postquant", "transquant"
]

suffixes = [
    "ique", "ien", "al", "el", "aire", "iste", "ique", "ide", "ose", "yle", "ure", "ion",
    "ance", "ence", "ité", "isme", "logue", "cratie", "phage", "vore", "phile", "phobe",
    "mane", "logue", "sophe", "gnome", "thèque", "scope", "mètre", "graphe", "phone",
    "drome", "nome", "thèque", "théque", "thécaire", "thécaire", "thécaire", "thécaire"
]

crypto_noms = [
    "bitcoin", "ethereum", "solana", "cardano", "polkadot", "cosmos", "avalanche", "algorand",
    "tezos", "hedera", "stellar", "ripple", "monero", "zcash", "dash", "decentraland", "sandbox",
    "axie", "enjin", "chiliz", "flow", "theta", "vechain", "kucoin", "binance", "coinbase",
    "kraken", "huobi", "okx", "bybit", "gate", "mexc", "ledger", "trezor", "metamask", "phantom",
    "trustwallet", "ordinals", "brc20", "runes", "stacks", "clarity", "unisat", "sats", "utxo",
    "segwit", "taproot", "bech32", "bip39", "erc20", "erc721", "erc1155", "soulbound", "layer2",
    "zk-snarks", "zk-starks", "plasma", "parachain", "kusama", "moonbeam", "astar", "acala"
]

mystiques = [
    "chaman", "druide", "prophète", "oracle", "mage", "alchimiste", "soufí", "derviche",
    "lama", "moine", "ermite", "saint", "gnostique", "kabbaliste", "rasoul", "wali",
    "fakir", "sannyasin", "ascète", "théurge", "voyant", "cosmocrate", "démiurge", "siddha",
    "bodhisattva", "bouddha", "brahmane", "khan", "calife", "clerc", "gourou", "templier",
    "franciscain", "zoroastrien", "ibn-arabi", "roumi", "rishi", "pandit", "tarik", "hanif"
]

lieux = [
    "nébuleuse", "abysse", "tesseract", "wormhole", "event horizon", "membrana", "brana",
    "calabi-yau", "orbifold", "conifold", "géon", "kerr", "schwarzschild", "minkowski",
    "euclide", "lorentz", "galilée", "newton", "planck", "subplanck", "supralumi", "sublumi",
    "tachyon", "bradyon", "luxon", "tardyon", "graviton", "électrofaible", "chromodynamique",
    "unifiée", "supersymétrie", "brana", "membrana", "calabi", "orbifold", "conifold", "géon"
]

verbes = [
    "pulsatilise", "fractalise", "quantifie", "entrelace", "dématérialise", "fissionne",
    "superpose", "diffraie", "interfère", "cohère", "glitche", "crypte", "encode", "décrypte",
    "transcende", "synchronise", "désynchronise", "résonne", "vibre", "oscille", "implose",
    "explose", "sublimise", "condense", "évapore", "ionise", "plasmafie", "noétise", "thanatise",
    "chtonise", "vorticise", "phréatise", "kaléidoscope", "protéiforme", "métastabilise",
    "liminalise", "démiurgise", "eschatologise", "médiumnise", "hypnagogise", "catalepsise"
]

concepts = [
    "entropie", "synchronicité", "causalité", "acausalité", "superposition", "entrelacement",
    "cohérence", "incohérence", "discrétisation", "continuité", "fuzziness", "crispness",
    "bayésianisme", "markovianité", "récursivité", "itération", "fractalité", "chaos",
    "laminarité", "turbulence", "granularité", "cristallinité", "amorphisme", "nanostructure",
    "mésoscopie", "macroscopie", "cosmologie", "subplanck", "planck", "supralumi", "sublumi",
    "tachyon", "bradyon", "luxon", "tardyon", "graviton", "électrofaible", "chromodynamique"
]

# === Générateurs par catégorie ===
def generer_adjectifs(n=3000):
    adjs = set()
    while len(adjs) < n:
        # Préfixe + suffixe
        adjs.add(random.choice(prefixes) + random.choice(suffixes))
        # Crypto + mystique
        adjs.add(random.choice(crypto_noms) + "-" + random.choice(mystiques))
        # Tech + mystique
        adjs.add(random.choice(["kernel", "daemon", "thread", "cache", "blockchain", "cloud", "glitch"]) + "-" + random.choice(mystiques))
        # Poétique
        if random.random() < 0.4:
            adjs.add(random.choice(["néo", "paléo", "hyper", "trans", "meta"]) + random.choice(["quantique", "chamanique", "soufique", "mystique"]))
    return sorted(list(adjs))[:n]

def generer_noms(n=1000):
    noms = set()
    while len(noms) < n:
        # Crypto + lieu
        noms.add(random.choice(crypto_noms).capitalize() + " " + random.choice(lieux).capitalize())
        # Mystique + concept
        noms.add(random.choice(mystiques).capitalize() + " de " + random.choice(concepts).capitalize())
        # Adjectif + nom abstrait
        noms.add(random.choice(generer_adjectifs(100)) + " " + random.choice(["système", "réseau", "flux", "nœud", "portail", "voile", "miroir", "éther", "plasma", "vide"]))
    return sorted(list(noms))[:n]

def generer_verbes(n=800):
    return [v for v in verbes * (n // len(verbes) + 1) if len(set(verbes * (n // len(verbes) + 1))) >= n][:n]

def generer_lieux(n=600):
    return [l.capitalize() for l in lieux * (n // len(lieux) + 1)][:n]

def generer_concepts(n=700):
    return [c.capitalize() for c in concepts * (n // len(concepts) + 1)][:n]

# === Génération complète ===
data = {
    "Adjectif": generer_adjectifs(3000),
    "Nom": generer_noms(1000),
    "Verbe": generer_verbes(800),
    "Lieu": generer_lieux(600),
    "Concept": generer_concepts(700)
}

# === Sauvegarde ===
with open("univers_lexical_complet.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Univers lexical généré !")
print(f"   Adjectifs : {len(data['Adjectif'])}")
print(f"   Noms      : {len(data['Nom'])}")
print(f"   Verbes    : {len(data['Verbe'])}")
print(f"   Lieux     : {len(data['Lieu'])}")
print(f"   Concepts  : {len(data['Concept'])}")
print("Fichier sauvegardé : univers_lexical_complet.json")
