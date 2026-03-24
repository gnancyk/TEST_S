def extracteur(text,debut,fin):
    return text[text.find(f"{debut}") + len(f"{debut}"):text.find(f"{fin}")]  