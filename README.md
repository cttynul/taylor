# Taylor
#### My lovely personal assistant.

![bot_pic](https://raw.githubusercontent.com/cttynul/taylor/main/gitpic/botpic.jpg) 

## How it works?
**Taylor** is just my lovely personal assistant, powered by [NLTK](https://www.nltk.org/) and [ChatterBot](https://github.com/gunthercox/ChatterBot) with some [custom italian corpus](https://github.com/cttynul/chatterbot-corpus)

She will learn everything you teach during a conversation, **warning** out of the box **Taylor** is a bit stupid and she can speak **only italian**.

## Usage
1. Create a ```config.json``` file in **Taylor** root directory like this:
```
{
    "token":"BotFather Token",
    "user":"Admin Telegram Nick, without 'at'",
    "phue":"IP adress of Philips Hue hub",
    "content_dirs":["/path/to/things/1", "/path/to/things/n"],
    "userid":[1234567],
    "meme_folder":"/path/to/meme/",
    "song_folder":"/path/to/voice_note/",
    "corpus_folder":"./corpus/"
}
```
2. Install all packages needed to run **Taylor**
```
# pip3 install -r requirements.txt
```
3. Put everything you want in **directory** mentioned in ```config.json```
4. Deploy as you wish, you can use **systemd** service ```taylorbot.service```
```
# cp taylorbot.service /etc/systemd/system/taylorbot.service
```
5. Edit **systemd service** according to your setup
```
# vim /etc/systemd/system/taylorbot.service
```
```
[Unit]
Description=Taylor Telegram Bot
After=network.target

[Service]
User=USERNAME_THAT_RUN_SERVICE
Group=USERGROUP_OF_USER
WorkingDirectory=/PATH/TO/ROOT/BOT/DIR
ExecStart= /bin/python3 bot.py
Restart=on-failure
RestartSec=5sec

[Install]
WantedBy=multi-user.target
```
5. **Reload** daemon list, **run** it and **enable**
```
# systemctl daemon-reload
```
```
# systemctl start taylorbot.service
```
```
# systemctl enable taylorbot.service
```
6. Enjoy **Tay Tay**

## License
```
                   Learning Only License License (LOL)

                      Copyright (c) 2020, cttynul
                          All rights reserved.

 *  The intended purpose of this code is educational only, and that purpose
    must be considered in any use or redistribution of the code or any
    modified version of the code. Any permissible change in License
    Agreement to any redistribution of this code, derivative or otherwise,
    must be done in good faith considering the original intent.

 *  You are not permitted to use this code or any modification of the code
    in any situation where original authorship is expected, or authorship
    is not able to be made clear in the use of the code. Use of this code
    directly for a homework assignment is explicitly prohibited.

 *  The Learning Only License is subordinate to any other accompanying License
    Agreement, and as such any prohibition or permission of use by accompanying
    License Agreements supersedes any permission or prohibition, respectively,
    provided by the Learning Only License.

 *  You may use this code freely, as is or modified, for any purpose not
    explicitly prohibited by this or any accompanying License Agreements, 
    including redistributing the original code and/or any modified version,
    provided such use is consistent with any other accompanying License 
    Agreements and you do the following:

    1.  Read through the code completely, including all of its comments.
    2.  Attempt to understand how it works.
    3.  Learn something from it.
    4.  Do not simply copy any portion of the code verbatim into another
        application; at the very least, add comments explaining what you are
        using, why you are using it, and where you obtained it.
    5.  Hold only yourself responsible, and not the original author or the 
        author of any modifications, for any bugs in your application that are
        the result of your failure to understand the code.
    6.  Do not hold the original author or author of any modifications
        responsible for bugs in your application that are the results of the
        author's mistakes.
    7.  Attempt to contact the responsible author and report any bugs found in
        the original code or any modifications, explaining what is wrong with
        the code and why it is a bug, so that the responsible author may learn
        from your experiences.
    8.  Keep the author(s)'s contact info, if provided or available, within the
        original or modified code so you can remember where it came from and to
        whom any bugs should be reported. If contact info is not available,
        keep a record of where the original code was obtained within the
        original or modified code.
    9.  Redistribute the original or modified code only if you have given due
        dilligence to understand it fully and can honestly attempt to answer 
        any questions about the code the person(s) to whom you give it may have.
    10. Redistribute a modified version of the code only after clearly marking
        the modifications you have made and adding your contact info in case
        you have introduced a bug into it and the recipient needs to contact you
        to report it.
    11. Do not get a bad attitude with anybody reporting bugs in your original
        or modified code.
    12. Attempt to fix any bugs for which you are responsible, seeking help to
        do so if necessary.
    13. Include a copy of this license with any source you distribute that
        contains the original or modified code. A copy of this license does not
        have to be included with any binaries if they are not distributed with
        the source code of that binary.
    14. If you make a profit from your application that contains the original
        or modified code, attempt to contact the author(s) and thank them for
        their help.
```
