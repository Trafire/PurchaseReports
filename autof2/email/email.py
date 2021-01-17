import win32com.client as win32

def emailer(text, subject, recipient, display=True):
    
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = recipient
    mail.Subject = subject
    mail.HTMLBody = text

    if display:
        mail.Display(True)
    else:
        mail.send()


def chart_html(title,headers,rows):
    '''
        (str, tup of strings, list of tup of str > str)
    '''
    columns = len(headers)
    title_row = '''<table>\n<tr><th colspan=%i>%s</th></tr>\n''' % (columns,title)
    column_row = '<tr>'
    for h in headers:
        column_row += '<th>%s</th>' % h
    column_row += '</tr>\n'
    body =''
    align = "left"
    for tr in rows:
        body += '<tr>'
        for td in tr:
            body += '<td align="%s">%s</td>' % (align,td)
            align = "center"
        body += '</tr>\n'
    body += '</table>'
    return title_row + column_row + body

def email_chart(title,headers,rows, subject, recipient,display=True):
    '''
        (str, tup of strings, list of tup of str -> str)
    '''
    text = chart_html(title,headers,rows)
    emailer(text, subject, recipient, display)

##email_chart('elmo',("price", "quantity","rating"), (("1.00","4","3"),("2.00","4","3"),("3.00","4","3.3"),("4.00","4",".95")),'Hello',"antoinewood@gmail.com")

##if __name__ == "__main__":    
##    msg = "<h1>HELLO WORLD</h1><img src=D:\\BuyProg\\new\\tropical_pics\\Ginger_Med_Pink.jpg></img>"
##    subject = "hello2"
##    recipient = "antoinewood@gmail.com"
##    emailer(msg, subject, recipient)
