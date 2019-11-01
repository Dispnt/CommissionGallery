from flask import Flask, render_template, json
from datetime import timedelta
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import json


def dictProcess(appendContent):
    form = NameForm()
    appendContent["url"] = form.url.data
    if form.thumbnailWidth.data != "" and form.thumbnailHeight.data != "":
        appendContent["thumbnailInfo"] = {
            "beginPointX": form.thumbnailBX.data,
            "beginPointY": form.thumbnailBY.data,
            "cutWidth": form.thumbnailWidth.data,
            "cutHeight": form.thumbnailHeight.data
        }
    appendContent["type"] = form.type.data
    appendContent["title"] = form.title.data
    appendContent["author"] = form.author.data


class NameForm(FlaskForm):
    id = StringField('id', validators=[DataRequired()])
    url = StringField('图床链接', validators=[DataRequired()])
    author = StringField('画师')
    type = StringField('类型')
    title = StringField('标题')
    thumbnailBX = StringField('起始X坐标')
    thumbnailBY = StringField('起始Y坐标')
    thumbnailWidth = StringField('选取宽度(px)')
    thumbnailHeight = StringField('选取高度(px)')
    submit = SubmitField('提交')


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

with open('gallery_list.json', encoding='utf-8') as f:
    gallery_JSON = json.load(f)


@app.route('/gallery_list')
def gallery_json():
    return json.dumps(gallery_JSON)


@app.route('/')
def index():
    return render_template('index.html', gallery_Json=gallery_JSON)


@app.route('/config')
def configpage():
    form = NameForm()
    return render_template('commissionConfig.html', gallery_Json=gallery_JSON, form=form)


@app.route('/config', methods=['GET', 'POST'])
def opForm():
    form = NameForm()
    if form.validate_on_submit():
        if form.submit.data:
            appendContent = {}
            if form.id.data != "New":
                appendContent["id"] = int(form.id.data) + 1
                dictProcess(appendContent)
                gallery_JSON["commissions"][int(form.id.data)] = appendContent
            else:
                appendContent["id"] = len(gallery_JSON["commissions"]) + 1
                dictProcess(appendContent)
                gallery_JSON["commissions"].append(appendContent)

            with open('gallery_list.json', 'w', encoding='utf-8') as f:
                json.dump(gallery_JSON, f, indent=4, ensure_ascii=False)
            return render_template('commissionConfig.html', gallery_Json=gallery_JSON, form=form)

        return ('', 204)


if __name__ == '__main__':
    app.run()
