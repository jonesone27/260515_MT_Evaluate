from sacrebleu.metrics import BLEU, CHRF, TER
# see https://docs.python.org/3/tutorial/inputoutput.html#tut-files 
# Note that the ref_lines items must be wrapped in another list (see https://pypi.org/project/sacrebleu/)

# NEXT: return the BLEU score/figures to FASTAPI

with open("data/europarl-v7de_100_EN_REF.txt", "r", encoding="utf8") as fref:
    ref_lines = fref.readlines()
    ref = [ref_lines]
    # i=1
    # for x in ref_lines:
    #     print(f"Ref {i}: {x}")
    #     i +=1
    # print(f"Ref text: {ref_lines}")

with open("data/europarl-v7de_100_EN_HYP.txt", "r", encoding="utf-8") as fhyp:
    hyp_lines = fhyp.readlines()
    # hyp_lines = [ln for ln in hyp_lines if ln.strip() != ""]
    # i=1
    # for x in hyp_lines:
    #     print(f"Hyp {i}: {x}")
    #     i +=1
    # # print(f"Machine translation: {hyp_lines}")

bleu = BLEU()

bscore = bleu.corpus_score(hyp_lines, ref)
print(f"Bleuscore: {bscore} \n")

# bsign = bleu.get_signature()
# print(bsign)