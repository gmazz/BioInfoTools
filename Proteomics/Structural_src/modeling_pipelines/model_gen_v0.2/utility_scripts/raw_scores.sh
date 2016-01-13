grep -r -H "MODELLER OBJECTIVE FUNCTION:" running | sed s'/REMARK   6 MODELLER OBJECTIVE FUNCTION:      //'g >> models_raw_scores.txt
