def viral_score(headline,summary,star=6,visual=7):
    words={"récord":12,"histórico":12,"remontada":10,"jonrón":8,"triple-doble":9,"nocaut":12,"golazo":10,"hat-trick":11,"sorpresa":7,"lesión":8}
    text=f"{headline} {summary}".lower();score=25+min(20,star*2)+min(20,visual*2)
    for k,v in words.items():
        if k in text: score+=v
    return min(100,score)
