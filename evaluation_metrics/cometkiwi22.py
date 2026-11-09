from comet import download_model, load_from_checkpoint
from models.evaluation_model import MTMetrics, COMETKIWIScore
from fastapi import HTTPException
# See: https://huggingface.co/Unbabel/wmt22-cometkiwi-da
# See: https://github.com/Unbabel/COMET#comet-models




class COMETKIWI:
    
    def __init__(self):
        self.path = download_model("Unbabel/wmt22-cometkiwi-da")
        self.model = load_from_checkpoint(self.path)

    def calc_ckiwi(self, src_list, hyp_list):
        data = []
        sent_scores = []


        # https://docs.python.org/3/builtins/functions.html#zip
        # align source and MT segments for proper COMETKIWI evaluation
        for src, hyp in zip(src_list, hyp_list):
            data.append(
                            {
                                "src": src,
                                "mt": hyp
                            }
                    
                        )

        # Calculate COMETKIWI sentence and overall scores
        # Change from GPU to CPU processing to allow for use on regular PCs 
        model_output = self.model.predict(data, batch_size=8, gpus=0, accelerator="cpu")

        print(f"COMETKIWI self.model:{self.model}")
        print(f"COMETKIWI self.model:{type(self.model)}")

        # https://docs.python.org/3/builtins/functions.html#enumerate
        # record segment score for each scr/mt pair:
        for i, score in enumerate(model_output.scores):
            sent_scores.append(
                {
                "segment_no": i,
                "segment_score": score
                }
            )

        # not sys_length = len(str(hyp_list)), as this would also count structural elements of the list, e.g. quotation marks and commas between list  items
        # Counting and summing up the characters within the individual list items:
        sys_length = sum(len(hyp) for hyp in hyp_list)
            
        src_length = sum(len(src) for src in src_list)    

        sys_score = model_output.system_score

        no_mtsegments_scored = len(hyp_list)

        return COMETKIWIScore(
            system_length=sys_length, 
            source_length=src_length,
            hyp_segment_qty=no_mtsegments_scored, 
            overall_score=sys_score, 
            segment_scores=sent_scores)

    

