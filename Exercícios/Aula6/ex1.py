import spacy

nlp = spacy.load("pt_core_news_lg")

texto = """China opõe-se à inaceitável eliminação de líderes nacionais

A China afirmou esta quinta-feira que “a eliminação de líderes nacionais e ataques contra alvos civis no Irão são absolutamente inaceitáveis”, após Israel ter morto o secretário do Conselho Supremo de Segurança Nacional do Irão e ex-presidente do parlamento, Ari Larijani.

O porta-voz do ministério dos Negócios Estrangeiros chinês Lin Jian afirmou, em conferência de imprensa, que Pequim “se opõe sistematicamente ao uso da força nas relações internacionais”.

Lin lamentou que “as chamas da guerra se estejam a expandir pelo Médio Oriente e que as tensões regionais estejam a aumentar”.

“Um cessar-fogo imediato e o fim das hostilidades representam a aspiração comum da comunidade internacional”, acrescentou o porta-voz, apelando “a todas as partes envolvidas” para que interrompam “imediatamente as operações militares e evitem que a situação regional se torne incontrolável”.

A Guarda Revolucionária iraniana afirmou na quarta-feira ter lançado um ataque com mísseis contra Telavive, em represália pela morte de Larijani, que era conselheiro do antigo líder supremo iraniano, Ali Khamenei, também morto numa operação israelita no início do atual conflito."""

doc = nlp(texto)

print("="*20, "Tokens", "="*20)

for entity in doc.ents:
    if entity.label_ in ["PER", "LOC", "ORG"]:
        print(entity, entity.label_)