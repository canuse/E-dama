# Frontend for auto-white-reimu

An UI interface for <a href="https://github.com/Ledenel/auto-white-reimu">Ledenel/auto-white-reimu</a>, which can check your mahjong records on tenhou.net and give advices.

No python environment is needed to execute the binary files, but **python 3.7** or later is recommended.

## Website

We also provided an website <a href="https://mjlog.canuse.xyz">mjlog.canuse.xyz</a> as a demo.

Note that this is only a demonstrating website, so DO NOT upload too many tasks at a time.

## Executable Files

### binary

You can simply download and execute the binary files like `E-white-reimu_*_win64.exe` from <a href="https://github.com/canuse/E-dama/releases">Releases</a> and then execute it.

The latest version is <a href="https://github.com/canuse/E-dama/releases/download/0.1/E-white-reimu_0.1_win64.exe">V0.1</a>.

### Python file

You can also download the python files from <a href="https://github.com/canuse/E-dama/releases">Releases</a>, however, you need to install several packages first.
1. Install `auto-white-reimu`. See <a href="https://github.com/Ledenel/auto-white-reimu"> here </a> for more instructions.
2. Install `pyqt5`, `sip`, `PyQt5-stubs` using `PIP`

## Deploy website

The source code of the website above is located in the `EReimuWeb` folder.

To deploy the website, you need to:
0. Clone the source code
1. Install `auto-white-reimu`, `django`, `apschduler`, `django-apschduler` using `PIP`
2. Get the setting file from <a href="https://github.com/canuse/E-dama/blob/c6ae9bdc00d1de65c96550e13aade9f13181fee5/EReimuWeb/EReimuWeb/settings.py">here</a>
3. Set the django secret key (setting.py, line 23). You can see instructions <a href="https://docs.djangoproject.com/en/2.2/ref/settings/#std:setting-SECRET_KEY">here</a>.
4. Set and migrate your own database
5. Modify the templates as you wish. They are located in `EReimuWeb/whiteReimu/templates`
6. Config the webserver like Nginx. The only thing need to be mentioned is that we use folder `EReimuWeb/whiteReimu/Records` to store reports, which were treated as static files.
An example of Nginx config is
```
location /history/{
alias /path/to/record/floder/;
}
location /{
//uwsgi settings
}
```

