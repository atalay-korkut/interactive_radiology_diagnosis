# CAP_radiology_reporting_website

A web interface for the RATCHET medical report generation model. <br>
RATCHET: https://github.com/farrell236/RATCHET/tree/master
### Usage

Download pretrained weights and put in `./checkpoints` folder.

- [ratchet_model_weights_202303111506.zip](http://www.doc.ic.ac.uk/~bh1511/ratchet_model_weights_202303111506.zip)
<br> Size: `1.5G` <br> MD5: `26ab19cf18908841320205e192dabe9f` <br>

Start django server to run the webapp:

"python manage.py runserver" in \interactive_radiology_diagnosis\cap_app

Choose a chest x-ray image to upload with a title and click upload.

Click Load Model or Generate to generate a report. (May take a couple of minutes to load the model the first time.)

You can modify the report and click Send Comment to send an input to the database.

Next time you click Generate, the model will use the input from the database to generate a report.

You can click Stats to see Output and Input statistics.




