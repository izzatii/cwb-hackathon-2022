from io import BytesIO
import os
import pandas as pd
from azure.core.exceptions import ResourceNotFoundError
from azure.ai.formrecognizer import FormRecognizerClient, DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

API_KEY = "API KEY"
ENDPOINT = "ENDPOINT"

doc = "10089434.pdf"
#doc = "GT WB - Job Description_IT Risk Lead (RMP)_v1.1.pdf"

form_recognizer_client = FormRecognizerClient(ENDPOINT, AzureKeyCredential(API_KEY))

with open(doc, "rb") as fd:
    f = fd.read()

poller = form_recognizer_client.begin_recognize_content(form=f)
result = poller.result()
form_pages = poller.result()

page = result[0]
# len(page.tables)

data = vars(page)
#print(page)

jd =[]

def format_bounding_box(bounding_box):
    if not bounding_box:
        return "N/A"
    return ", ".join(["[{}, {}]".format(p.x, p.y) for p in bounding_box])

for idx, content in enumerate(form_pages):
    print("----Recognizing content from page #{}----".format(idx+1))
    print("Page has width: {} and height: {}, measured with unit: {}".format(
        content.width,
        content.height,
        content.unit
    ))
    for table_idx, table in enumerate(content.tables):
        print("Table # {} has {} rows and {} columns".format(table_idx, table.row_count, table.column_count))
        print("Table # {} location on page: {}".format(table_idx, format_bounding_box(table.bounding_box)))
        for cell in table.cells:
            print("...Cell[{}][{}] has text '{}' within bounding box '{}'".format(
                cell.row_index,
                cell.column_index,
                cell.text,
                format_bounding_box(cell.bounding_box)
            ))

    for line_idx, line in enumerate(content.lines):
        print("Line # {} has word count '{}' and text '{}' within bounding box '{}'".format(
            line_idx,
            len(line.words),
            line.text,
            format_bounding_box(line.bounding_box)
        ))
        if line.appearance:
            if line.appearance.style_name == "handwriting" and line.appearance.style_confidence > 0.8:
                print("Text line '{}' is handwritten and might be a signature.".format(line.text))
        for word in line.words:
            print("...Word '{}' has a confidence of {}".format(word.text, word.confidence))
            jd.append([word.text])
    
    if content.selection_marks is not None:
        for selection_mark in content.selection_marks:
            print("Selection mark is '{}' within bounding box '{}' and has a confidence of {}".format(
                selection_mark.state,
                format_bounding_box(selection_mark.bounding_box),
                selection_mark.confidence
    
        ))
    print("----------------------------------------")


df_jd = pd.DataFrame(data=jd,columns=['keywords'])
df_jd.to_csv('jd.csv',index=False)
print('JD Keywords extracted')
