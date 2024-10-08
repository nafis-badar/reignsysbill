from django.core import serializers
import json
import datetime



def get_clear_array(rowdata):
    jsondata = serializers.serialize('json', rowdata)
    data = json.loads(jsondata)
    result = []
    for obj in data:
        obj['fields']['id'] = obj['pk']
        result.append(obj['fields'])

    return result


def get_clear_object(rowdata):
    jsondata = serializers.serialize('json', [rowdata, ])
    data = json.loads(jsondata)
    result = []
    for obj in data:
        obj['fields']['id'] = obj['pk']
        result.append(obj['fields'])

    return result[0]


def number_to_word(number):
    def get_word(n):
        words={ 0:"", 1:"One", 2:"Two", 3:"Three", 4:"Four", 5:"Five", 6:"Six", 7:"Seven", 8:"Eight", 9:"Nine", 10:"Ten", 11:"Eleven", 12:"Twelve", 13:"Thirteen", 14:"Fourteen", 15:"Fifteen", 16:"Sixteen", 17:"Seventeen", 18:"Eighteen", 19:"Nineteen", 20:"Twenty", 30:"Thirty", 40:"Forty", 50:"Fifty", 60:"Sixty", 70:"Seventy", 80:"Eighty", 90:"Ninty" }
        if n<=20:
            return words[n]
        else:
            ones=n%10
            tens=n-ones
            return words[tens]+" "+words[ones]
            
    def get_all_word(n):
        d = [100, 10, 100, 100]
        v = ["", "Hundred And", "Thousand", "lakh"]
        w = []
        for i, x in zip(d, v):
            t = get_word(n % i)
            if t != "":
                t += " "+x
            w.append(t.rstrip(" "))
            n = n//i
        w.reverse()
        w = ' '.join(w).strip()
        if w.endswith("And"):
            w = w[:-3]
        return w

    arr = str(number).split(".")
    number = int(arr[0])
    crore = number//10000000
    number = number % 10000000
    word = ""
    if crore > 0:
        word += get_all_word(crore)
        word += " crore "
    word += get_all_word(number).strip()+" Rupees"
    if len(arr) > 1:
        if len(arr[1]) == 1:
            arr[1] += "0"
        if int(arr[1]) == 0:
            return word
        else:
            word += " and "+get_all_word(int(arr[1]))+" paisa"
    return word


def format_float(number):
    float_n = float(number)
    format_float_number = "{:.2f}".format(float_n)
    return format_float_number

def datetime_fomat(date_var):
    date_formatted = datetime.datetime.strptime(date_var,'%Y-%m-%d').strftime('%d-%m-%Y')
    return date_formatted