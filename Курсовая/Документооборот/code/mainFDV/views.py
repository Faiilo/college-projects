from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import DatasetOtchet, PracType, DocumentTemplate
from docxtpl import DocxTemplate
import os
from django.conf import settings
from django.http import HttpResponse
import tempfile
import re

def format_date_for_doc(date_string):
    """
    Преобразует дату из формата ДД.ММ.ГГГГ в формат "День" Месяц ГГГГ
    Пример: "02.12.2025" -> "2 декабря 2025"
    """
    if not date_string:
        return ""
    
    try:
        # Разбираем дату
        if '.' in date_string:
            parts = date_string.split('.')
            day = parts[0]
            month = parts[1]
            year = parts[2]
        elif '-' in date_string:
            parts = date_string.split('-')
            day = parts[2]
            month = parts[1]
            year = parts[0]
        else:
            return date_string
        
        # Убираем ведущий ноль у дня
        day = str(int(day))
        
        # Названия месяцев в родительном падеже
        months_genitive = {
            '01': 'января', '02': 'февраля', '03': 'марта', '04': 'апреля',
            '05': 'мая', '06': 'июня', '07': 'июля', '08': 'августа',
            '09': 'сентября', '10': 'октября', '11': 'ноября', '12': 'декабря'
        }
        
        month_name = months_genitive.get(month, month)
        
        return f"{day} {month_name} {year}"
    
    except Exception as e:
        return date_string


def get_day_from_date(date_string):
    """Получает день из даты без ведущего нуля"""
    if not date_string:
        return ""
    try:
        if '.' in date_string:
            return str(int(date_string.split('.')[0]))
        elif '-' in date_string:
            return str(int(date_string.split('-')[2]))
    except:
        pass
    return ""


def get_month_name_from_date(date_string):
    """Получает название месяца в родительном падеже"""
    if not date_string:
        return ""
    try:
        if '.' in date_string:
            month = date_string.split('.')[1]
        elif '-' in date_string:
            month = date_string.split('-')[1]
        else:
            return ""
        
        months_genitive = {
            '01': 'января', '02': 'февраля', '03': 'марта', '04': 'апреля',
            '05': 'мая', '06': 'июня', '07': 'июля', '08': 'августа',
            '09': 'сентября', '10': 'октября', '11': 'ноября', '12': 'декабря'
        }
        return months_genitive.get(month, month)
    except:
        return ""


def get_year_from_date(date_string):
    """Получает год из даты"""
    if not date_string:
        return ""
    try:
        if '.' in date_string:
            return date_string.split('.')[2]
        elif '-' in date_string:
            return date_string.split('-')[0]
    except:
        pass
    return ""


# ========== ФУНКЦИИ ДЛЯ ОБРАБОТКИ ТЕКСТА ==========

def normalize_prac_type_for_title(prac_type):
    """
    Преобразует тип практики для титульного листа (родительный падеж, ВЕРХНИЙ РЕГИСТР)
    "Производственная" -> "ПРОИЗВОДСТВЕННОЙ"
    "Учебная" -> "УЧЕБНОЙ"
    """
    if not prac_type:
        return "ПРОИЗВОДСТВЕННОЙ"
    
    prac_type_lower = prac_type.lower()
    
    if prac_type_lower == "производственная":
        return "ПРОИЗВОДСТВЕННОЙ"
    elif prac_type_lower == "учебная":
        return "УЧЕБНОЙ"
    else:
        return prac_type.upper()


def normalize_prac_type_for_sentence(prac_type, case='genitive'):
    """
    Преобразует тип практики для предложений
    case: 'genitive' - родительный падеж (производственной/учебной)
          'dative' - дательный падеж (производственной/учебной)
    """
    if not prac_type:
        if case == 'genitive':
            return "производственной"
        else:
            return "производственной"
    
    prac_type_lower = prac_type.lower()
    
    if case == 'genitive':
        # Родительный падеж: производственной, учебной
        if prac_type_lower == "производственная":
            return "производственной"
        elif prac_type_lower == "учебная":
            return "учебной"
        else:
            return prac_type_lower
    else:
        # Дательный падеж (тоже производственной/учебной в русском языке)
        if prac_type_lower == "производственная":
            return "производственной"
        elif prac_type_lower == "учебная":
            return "учебной"
        else:
            return prac_type_lower


def normalize_prac_type_for_accusative(prac_type):
    """
    Преобразует тип практики в винительный падеж (кого? что?)
    "Производственная" -> "производственную"
    "Учебная" -> "учебную"
    """
    if not prac_type:
        return "производственную"
    
    prac_type_lower = prac_type.lower()
    
    if prac_type_lower == "производственная":
        return "производственную"
    elif prac_type_lower == "учебная":
        return "учебную"
    else:
        return prac_type_lower


def to_genitive_simple(full_name):
    """
    Преобразует ФИО в родительный падеж
    Филенко Дмитрий Владиславович -> Филенко Дмитрия Владиславовича
    """
    if not full_name or len(full_name.strip()) == 0:
        return ""
    
    def transform_last_name(name):
        """Преобразует фамилию в родительный падеж"""
        if not name:
            return name
        
        # Фамилии на -ко (Филенко, Шевченко и т.д.) не склоняются
        if name.endswith('ко'):
            return name
        
        # Фамилии на -о, -е, -и, -у, -ю не склоняются
        if name.endswith(('о', 'е', 'и', 'у', 'ю', 'ы', 'э')):
            return name
        
        # Фамилии на -а, -я
        if name.endswith('а'):
            return name[:-1] + 'ы'
        if name.endswith('я'):
            return name[:-1] + 'и'
        
        # Фамилии на -ий, -ый, -ой
        if name.endswith('ий'):
            return name[:-2] + 'его'
        if name.endswith('ый'):
            return name[:-2] + 'ого'
        if name.endswith('ой'):
            return name[:-2] + 'ого'
        
        # Фамилии на -ь
        if name.endswith('ь'):
            return name[:-1] + 'я'
        
        # Фамилии на -ж, -ч, -ш, -щ, -ц
        if name.endswith(('ж', 'ч', 'ш', 'щ', 'ц')):
            return name + 'а'
        
        # Обычные фамилии (на согласную)
        return name + 'а'
    
    def transform_first_name(name):
        """Преобразует имя в родительный падеж"""
        if not name:
            return name
        
        # Исключения
        exceptions = {
            'лев': 'льва', 'павел': 'павла', 'илья': 'ильи',
            'никита': 'никиты', 'фома': 'фомы', 'лука': 'луки',
            'дима': 'димы', 'дмитрий': 'дмитрия'
        }
        
        name_lower = name.lower()
        if name_lower in exceptions:
            return exceptions[name_lower].capitalize() if name[0].isupper() else exceptions[name_lower]
        
        # Имена на -а, -я
        if name.endswith('а'):
            return name[:-1] + 'ы'
        if name.endswith('я'):
            return name[:-1] + 'и'
        
        # Имена на -ий (Дмитрий, Валерий)
        if name.endswith('ий'):
            return name[:-2] + 'ия'
        
        # Имена на -ей (Андрей, Сергей)
        if name.endswith('ей'):
            return name[:-2] + 'ея'
        
        # Имена на -ь (Игорь)
        if name.endswith('ь'):
            return name[:-1] + 'я'
        
        # Имена на -й (Алексей)
        if name.endswith('й'):
            return name[:-1] + 'я'
        
        # Обычные имена
        return name + 'а'
    
    def transform_middle_name(name):
        """Преобразует отчество в родительный падеж"""
        if not name:
            return name
        
        # Отчества на -вич, -вна
        if name.endswith('вич'):
            return name + 'а'
        if name.endswith('вна'):
            return name[:-1] + 'ы'
        
        # Отчества на -ич
        if name.endswith('ич'):
            return name + 'а'
        
        # Отчества на -чна
        if name.endswith('чна'):
            return name[:-1] + 'ы'
        
        # Отчества на -овна, -евна
        if name.endswith('овна'):
            return name[:-1] + 'ы'
        if name.endswith('евна'):
            return name[:-1] + 'ы'
        
        # Обычные отчества
        if name.endswith('а'):
            return name[:-1] + 'ы'
        
        return name + 'а'
    
    parts = full_name.split()
    
    if len(parts) >= 1:
        last_name = transform_last_name(parts[0])
    else:
        last_name = ""
    
    if len(parts) >= 2:
        first_name = transform_first_name(parts[1])
    else:
        first_name = ""
    
    if len(parts) >= 3:
        middle_name = transform_middle_name(parts[2])
    else:
        middle_name = ""
    
    # Собираем результат
    result_parts = []
    if last_name:
        result_parts.append(last_name)
    if first_name:
        result_parts.append(first_name)
    if middle_name:
        result_parts.append(middle_name)
    
    return " ".join(result_parts)


def to_dative_simple(full_name):
    """
    Преобразует ФИО в дательный падеж (кому? чему?)
    Филенко Дмитрий Владиславович -> Филенко Дмитрию Владиславовичу
    """
    if not full_name or len(full_name.strip()) == 0:
        return ""
    
    def transform_last_name_dative(name):
        """Преобразует фамилию в дательный падеж"""
        if not name:
            return name
        
        # Фамилии на -ко не склоняются
        if name.endswith('ко'):
            return name
        
        # Фамилии на -а, -я
        if name.endswith('а'):
            return name[:-1] + 'е'
        if name.endswith('я'):
            return name[:-1] + 'е'
        
        # Фамилии на -ий, -ый, -ой
        if name.endswith('ий'):
            return name[:-2] + 'ему'
        if name.endswith('ый'):
            return name[:-2] + 'ому'
        if name.endswith('ой'):
            return name[:-2] + 'ому'
        
        # Обычные фамилии (на согласную)
        return name + 'у'
    
    def transform_first_name_dative(name):
        """Преобразует имя в дательный падеж"""
        if not name:
            return name
        
        # Исключения
        exceptions = {
            'лев': 'льву', 'павел': 'павлу', 'илья': 'илье',
            'никита': 'никите', 'фома': 'фоме', 'лука': 'луке',
            'дима': 'диме', 'дмитрий': 'дмитрию', 'андрей': 'андрею',
            'сергей': 'сергею', 'алексей': 'алексею'
        }
        
        name_lower = name.lower()
        if name_lower in exceptions:
            return exceptions[name_lower].capitalize() if name[0].isupper() else exceptions[name_lower]
        
        # Имена на -а, -я
        if name.endswith('а'):
            return name[:-1] + 'е'
        if name.endswith('я'):
            return name[:-1] + 'е'
        
        # Имена на -ий
        if name.endswith('ий'):
            return name[:-2] + 'ию'
        
        # Имена на -ей
        if name.endswith('ей'):
            return name[:-2] + 'ею'
        
        # Имена на -ь
        if name.endswith('ь'):
            return name[:-1] + 'ю'
        
        # Имена на -й
        if name.endswith('й'):
            return name[:-1] + 'ю'
        
        # Обычные имена
        return name + 'у'
    
    def transform_middle_name_dative(name):
        """Преобразует отчество в дательный падеж"""
        if not name:
            return name
        
        # Отчества на -вич, -вна
        if name.endswith('вич'):
            return name + 'у'
        if name.endswith('вна'):
            return name[:-1] + 'е'
        
        # Отчества на -ич
        if name.endswith('ич'):
            return name + 'у'
        
        # Обычные отчества
        if name.endswith('а'):
            return name[:-1] + 'е'
        
        return name + 'у'
    
    parts = full_name.split()
    
    if len(parts) >= 1:
        last_name = transform_last_name_dative(parts[0])
    else:
        last_name = ""
    
    if len(parts) >= 2:
        first_name = transform_first_name_dative(parts[1])
    else:
        first_name = ""
    
    if len(parts) >= 3:
        middle_name = transform_middle_name_dative(parts[2])
    else:
        middle_name = ""
    
    # Собираем результат
    result_parts = []
    if last_name:
        result_parts.append(last_name)
    if first_name:
        result_parts.append(first_name)
    if middle_name:
        result_parts.append(middle_name)
    
    return " ".join(result_parts)


def shorten_fio(full_name):
    """
    Преобразует полное ФИО в формат "Фамилия И.О."
    Пример: "Жирнова Юлия Витальевна" -> "Жирнова Ю.В."
    """
    if not full_name or len(full_name.strip()) == 0:
        return ""
    
    parts = full_name.split()
    
    if len(parts) >= 1:
        last_name = parts[0]
    else:
        return ""
    
    if len(parts) >= 2:
        first_initial = parts[1][0].upper() + "."
    else:
        first_initial = ""
    
    if len(parts) >= 3:
        middle_initial = parts[2][0].upper() + "."
    else:
        middle_initial = ""
    
    result = last_name
    if first_initial:
        result += " " + first_initial
    if middle_initial:
        result += middle_initial
    
    return result


def mainfSDS(request):
    return HttpResponse('app mainFDV')

def logoutf(request):
    logout(request)
    return redirect('/login/')


def register(request):
    if request.method == "GET":
        return render(request, "register.html", {"form": UserCreationForm()})
    else: 
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                request.POST['username'],
                password=request.POST['password1']
            )
            user.save()
            DatasetOtchet.objects.create(user=user)
            login(request, user)
            return redirect('/profile/')
        else:
            messages.error(request, 'Пароли не совпадают')
            return render(request, "register.html", {"form": UserCreationForm()})


def loginf(request): 
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Вы вошли как {username}')
                return redirect('/profile/')
            else:
                messages.error(request, 'Неправильное имя пользователя или пароль')
        else:
            messages.error(request, 'Неправильное имя пользователя или пароль')
    
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def profile(request):
    user_report, created = DatasetOtchet.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        if request.POST.get('familia'):
            user_report.familia = request.POST['familia']
        if request.POST.get('name'):
            user_report.name = request.POST['name']
        if request.POST.get('otchestvo'):
            user_report.otchestvo = request.POST['otchestvo']
        if request.POST.get('tip'):
            try:
                user_report.prac_type = PracType.objects.get(type_name=request.POST['tip'])
            except PracType.DoesNotExist:
                pass
        if request.POST.get('module'):
            user_report.module = request.POST['module']
        if request.POST.get('specialization'):
            user_report.specialization = request.POST['specialization']
        if request.POST.get('kurs'):
            user_report.kurs = request.POST['kurs']
        if request.POST.get('group'):
            user_report.group = request.POST['group']
        if request.POST.get('hours'):
            try:
                user_report.hours = int(request.POST['hours'])
            except ValueError:
                user_report.hours = None
        if request.POST.get('mesto'):
            user_report.mesto = request.POST['mesto']
        if request.POST.get('address'):
            user_report.address = request.POST['address']
        if request.POST.get('mdk'):
            user_report.mdk = request.POST['mdk']
        if request.POST.get('begin_date'):
            date_parts = request.POST['begin_date'].split('-')
            if len(date_parts) == 3:
                user_report.date_begin = f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]}"
        if request.POST.get('finish_date'):
            date_parts = request.POST['finish_date'].split('-')
            if len(date_parts) == 3:
                user_report.date_finish = f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]}"
        if request.POST.get('head1'):
            user_report.head1 = request.POST['head1']
        if request.POST.get('head2'):
            user_report.head2 = request.POST['head2']
        if request.POST.get('ruc_pract'):
            user_report.ruc_pract = request.POST['ruc_pract']
        if request.POST.get('year'):
            user_report.year = request.POST['year']
        
        user_report.save()
        messages.success(request, 'Данные успешно сохранены!')
        return redirect('/profile/')
    
    # Обработка GET запроса (показываем форму)
    begin_date_for_input = ''
    finish_date_for_input = ''
    
    if user_report.date_begin:
        try:
            date_parts = user_report.date_begin.split('.')
            if len(date_parts) == 3:
                begin_date_for_input = f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}"
        except:
            pass
    
    if user_report.date_finish:
        try:
            date_parts = user_report.date_finish.split('.')
            if len(date_parts) == 3:
                finish_date_for_input = f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}"
        except:
            pass
    
    prac_types = PracType.objects.all()
    
    # Проверяем наличие шаблонов
    templates_exist = {
        'title': DocumentTemplate.objects.filter(doc_type='title').exists(),
        'assignment': DocumentTemplate.objects.filter(doc_type='assignment').exists(),
        'diary': DocumentTemplate.objects.filter(doc_type='diary').exists(),
    }
    
    return render(request, "profile.html", {
        "user_report": user_report,
        "prac_types": prac_types,
        "begin_date_for_input": begin_date_for_input,
        "finish_date_for_input": finish_date_for_input,
        "templates_exist": templates_exist
    })
    user_report, created = DatasetOtchet.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        if request.POST.get('familia'):
            user_report.familia = request.POST['familia']
        if request.POST.get('name'):
            user_report.name = request.POST['name']
        if request.POST.get('otchestvo'):
            user_report.otchestvo = request.POST['otchestvo']
        if request.POST.get('tip'):
            try:
                user_report.prac_type = PracType.objects.get(type_name=request.POST['tip'])
            except PracType.DoesNotExist:
                pass
        if request.POST.get('module'):
            user_report.module = request.POST['module']
        if request.POST.get('specialization'):
            user_report.specialization = request.POST['specialization']
        if request.POST.get('kurs'):
            user_report.kurs = request.POST['kurs']
        if request.POST.get('group'):
            user_report.group = request.POST['group']
        if request.POST.get('hours'):
            try:
                user_report.hours = int(request.POST['hours'])
            except ValueError:
                user_report.hours = None
        if request.POST.get('mesto'):
            user_report.mesto = request.POST['mesto']
        if request.POST.get('address'):
            user_report.address = request.POST['address']
        if request.POST.get('mdk'):  # НОВОЕ ПОЛЕ
            user_report.mdk = request.POST['mdk']
        if request.POST.get('begin_date'):
            date_parts = request.POST['begin_date'].split('-')
            if len(date_parts) == 3:
                user_report.date_begin = f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]}"
        if request.POST.get('finish_date'):
            date_parts = request.POST['finish_date'].split('-')
            if len(date_parts) == 3:
                user_report.date_finish = f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]}"
        if request.POST.get('head1'):
            user_report.head1 = request.POST['head1']
        if request.POST.get('head2'):
            user_report.head2 = request.POST['head2']
        if request.POST.get('ruc_pract'):
            user_report.ruc_pract = request.POST['ruc_pract']
        if request.POST.get('year'):
            user_report.year = request.POST['year']
        
        user_report.save()
        messages.success(request, 'Данные успешно сохранены!')
        return redirect('/profile/')


@login_required
def generate_all_documents(request):
    """
    Генерация всех документов (титульный лист, задание, дневник) и упаковка в ZIP
    """
    from datetime import datetime
    import tempfile
    import os
    import zipfile
    from io import BytesIO
    
    # Получаем данные пользователя
    user_report = get_object_or_404(DatasetOtchet, user=request.user)
    
    # Проверяем, что у пользователя заполнены обязательные поля
    if not user_report.familia or not user_report.name:
        messages.error(request, 'Пожалуйста, заполните фамилию и имя в профиле перед генерацией документов.')
        return redirect('/profile/')
    
    # Проверяем наличие всех шаблонов
    templates = {
        'title': DocumentTemplate.objects.filter(doc_type='title').first(),
        'assignment': DocumentTemplate.objects.filter(doc_type='assignment').first(),
        'diary': DocumentTemplate.objects.filter(doc_type='diary').first(),
    }
    
    missing_templates = [name for name, tmpl in templates.items() if not tmpl]
    if missing_templates:
        messages.error(request, f'Отсутствуют шаблоны: {", ".join(missing_templates)}. Обратитесь к администратору.')
        return redirect('/profile/')
    
    # Функция для разбора даты
    def parse_date(date_string):
        if not date_string:
            return {'day': '', 'month': '', 'year': ''}
        try:
            if '.' in date_string:
                parts = date_string.split('.')
                if len(parts) == 3:
                    return {
                        'day': parts[0],
                        'month': parts[1],
                        'year': parts[2]
                    }
            elif '-' in date_string:
                parts = date_string.split('-')
                if len(parts) == 3:
                    return {
                        'day': parts[2],
                        'month': parts[1],
                        'year': parts[0]
                    }
        except:
            pass
        return {'day': '', 'month': '', 'year': ''}
    
    # Разбираем даты
    date_begin_parts = parse_date(user_report.date_begin)
    date_finish_parts = parse_date(user_report.date_finish)
    
    # Названия месяцев на русском
    months = {
        '01': 'января', '02': 'февраля', '03': 'марта', '04': 'апреля',
        '05': 'мая', '06': 'июня', '07': 'июля', '08': 'августа',
        '09': 'сентября', '10': 'октября', '11': 'ноября', '12': 'декабря'
    }
    
    month_begin_text = months.get(date_begin_parts['month'], date_begin_parts['month'])
    month_finish_text = months.get(date_finish_parts['month'], date_finish_parts['month'])

    # Получаем полное название модуля и его код
    module_full = user_report.module or ''
    module_code_match = re.search(r'ПМ\.\d+', module_full)
    module_code = module_code_match.group(0) if module_code_match else module_full
    
    # Получаем тип практики
    prac_type_name = user_report.prac_type.type_name if user_report.prac_type else 'Производственная'
    
    # Преобразуем тип практики для разных мест
    prac_type_for_title = normalize_prac_type_for_title(prac_type_name)
    prac_type_genitive = normalize_prac_type_for_sentence(prac_type_name, case='genitive')
    prac_type_dative = normalize_prac_type_for_sentence(prac_type_name, case='dative')
    prac_type_accusative = normalize_prac_type_for_accusative(prac_type_name)
    
    # Полное ФИО
    full_name = f"{user_report.familia} {user_report.name} {user_report.otchestvo}".strip()
    
    # ФИО в разных падежах
    full_name_genitive = to_genitive_simple(full_name)
    full_name_dative = to_dative_simple(full_name)
    
    # Сокращенные ФИО для руководителей
    head1_short = shorten_fio(user_report.head1)
    head2_short = shorten_fio(user_report.head2)
    ruc_pract_short = shorten_fio(user_report.ruc_pract)
    
    # Форматированные даты
    date_begin_formatted = format_date_for_doc(user_report.date_begin)
    date_finish_formatted = format_date_for_doc(user_report.date_finish)
    
    # Получаем компоненты дат
    begin_day = get_day_from_date(user_report.date_begin)
    begin_month = get_month_name_from_date(user_report.date_begin)
    begin_year = get_year_from_date(user_report.date_begin)
    
    finish_day = get_day_from_date(user_report.date_finish)
    finish_month = get_month_name_from_date(user_report.date_finish)
    finish_year = get_year_from_date(user_report.date_finish)
    
    # ФУНКЦИЯ ДЛЯ ОЧИСТКИ ДАННЫХ
    def clean_text(text):
        """Очищает текст от символов, которые могут повредить DOCX"""
        if not text:
            return ""
        # Преобразуем в строку
        text = str(text)
        # Удаляем недопустимые символы для XML
        import re
        # Удаляем control characters кроме \n, \r, \t
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
        # Ограничиваем длину (Word может не выдержать слишком длинные строки)
        if len(text) > 5000:
            text = text[:5000] + "..."
        return text
    
    # Подготовка данных для шаблона с очисткой
    context = {
        'fio': clean_text(full_name),
        'familia': clean_text(user_report.familia or ''),
        'name': clean_text(user_report.name or ''),
        'otchestvo': clean_text(user_report.otchestvo or ''),
        'fio_genitive': clean_text(full_name_genitive),
        'fio_dative': clean_text(full_name_dative),
        'tip': clean_text(prac_type_name),
        'tip_title': clean_text(prac_type_for_title),
        'tip_genitive': clean_text(prac_type_genitive),
        'tip_dative': clean_text(prac_type_dative),
        'tip_accusative': clean_text(prac_type_accusative),
        'mdk': clean_text(user_report.mdk or ''),
        'head1': clean_text(user_report.head1 or '_________________________'),
        'head2': clean_text(user_report.head2 or '_________________________'),
        'ruc_pract': clean_text(user_report.ruc_pract or '_________________________'),
        'head1_short': clean_text(head1_short or '_________________________'),
        'head2_short': clean_text(head2_short or '_________________________'),
        'ruc_pract_short': clean_text(ruc_pract_short or '_________________________'),
        'module': clean_text(module_full),
        'module_code': clean_text(module_code),
        'specialization': clean_text(user_report.specialization or '09.02.07 "Информационные системы и программирование"'),
        'kurs': clean_text(str(user_report.kurs or '2')),
        'group': clean_text(user_report.group or ''),
        'date_begin': clean_text(user_report.date_begin or ''),
        'date_finish': clean_text(user_report.date_finish or ''),
        'day_begin': clean_text(date_begin_parts['day']),
        'mesto': clean_text(user_report.mesto or ''),
        'address': clean_text(user_report.address or ''),
        'month_begin': clean_text(month_begin_text),
        'year_begin': clean_text(date_begin_parts['year']),
        'day_finish': clean_text(date_finish_parts['day']),
        'month_finish': clean_text(month_finish_text),
        'year_finish': clean_text(date_finish_parts['year']),
        'date_begin_formatted': clean_text(date_begin_formatted),
        'date_finish_formatted': clean_text(date_finish_formatted),
        'begin_day': clean_text(begin_day),
        'begin_month': clean_text(begin_month),
        'begin_year': clean_text(begin_year),
        'finish_day': clean_text(finish_day),
        'finish_month': clean_text(finish_month),
        'finish_year': clean_text(finish_year),
        'year': clean_text(str(user_report.year or datetime.now().year)),
        'username': clean_text(request.user.username),
        'name_org': clean_text('ГБПОУ МО «Люберецкий техникум имени Героя Советского Союза, летчика-космонавта Ю.А.Гагарина»'),
        'address_org': clean_text('Московская область, г. Люберцы'),
        'phone_org': clean_text('+7 (495) XXX-XX-XX'),
        'email_org': clean_text('info@lubertsy-teh.ru'),
        'sphere': clean_text('Профессиональное образование'),
        'year_foundation': clean_text('19XX'),
        'form_ownership': clean_text('Государственное бюджетное учреждение'),
        'hours': clean_text(str(user_report.hours or '36')),
        'history_org': clean_text('_________________________'),
        'godovoy_otchet': clean_text('_________________________'),
        'uslugi_org': clean_text('Образовательные услуги по подготовке специалистов СПО'),
        'achievments_org': clean_text('_________________________'),
        'name_docher': clean_text('_________________________'),
        'address_docher': clean_text('_________________________'),
        'phone_docher': clean_text('_________________________'),
        'email_docher': clean_text('_________________________'),
        'name_podrazdel': clean_text('Отдел информационных технологий'),
        'head_podrazdel': clean_text('_________________________'),
        'fio_head_practice': clean_text(user_report.ruc_pract or '_________________________'),
        'kurator_phone': clean_text('_________________________'),
        'kurator_email': clean_text('_________________________'),
        'struk_and_func': clean_text('_________________________'),
        'goal_pract': clean_text(f'{prac_type_genitive} практической подготовки'),
        'prof_kompetentsii': clean_text('''
- ПК 11.1 Осуществлять сбор, обработку и анализ информации для проектирования баз данных
- ПК 11.2 Проектировать базу данных на основе анализа предметной области
- ПК 11.3 Разрабатывать объекты базы данных в соответствии с результатами анализа предметной области
- ПК 11.4 Реализовывать базу данных в конкретной системе управления базами данных
- ПК 11.5 Администрировать базы данных
- ПК 11.6 Защищать информацию в базе данных с использованием технологии защиты информации
        '''),
        'obsh_kompetentsii': clean_text('''
- ОК 01. Выбирать способы решения задач профессиональной деятельности применительно к различным контекстам
- ОК 02. Использовать современные средства поиска, анализа и интерпретации информации 
- ОК 03. Планировать и реализовывать собственное профессиональное и личностное развитие
- ОК 04. Эффективно взаимодействовать и работать в коллективе и команде
- ОК 05. Осуществлять устную и письменную коммуникацию на государственном языке
- ОК 06. Проявлять гражданско-патриотическую позицию, демонстрировать осознанное поведение
- ОК 07. Содействовать сохранению окружающей среды, ресурсосбережению
- ОК 08. Использовать средства физической культуры для сохранения и укрепления здоровья
- ОК 09. Пользоваться профессиональной документацией на государственном и иностранном языках
        '''),
    }
    
    doc_names_map = {
        'title': 'Титульный_лист',
        'assignment': 'Задание',
        'diary': 'Дневник'
    }
    
    try:
        # Создаем ZIP архив в памяти
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Генерируем каждый документ
            for doc_type, template_obj in templates.items():
                if not template_obj:
                    continue
                
                template_path = template_obj.template_file.path
                
                # Создаем временный файл для документа
                with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp_file:
                    tmp_path = tmp_file.name
                
                try:
                    # Рендерим документ
                    doc = DocxTemplate(template_path)
                    doc.render(context)
                    doc.save(tmp_path)
                    
                    # Проверяем, что файл не пустой
                    if os.path.getsize(tmp_path) < 100:
                        raise Exception(f"Файл {doc_type} слишком маленький, возможно ошибка рендеринга")
                    
                    # Читаем файл
                    with open(tmp_path, 'rb') as f:
                        docx_data = f.read()
                    
                    # Добавляем в ZIP
                    inner_name = f"{doc_names_map.get(doc_type, doc_type)}_{user_report.familia}_{user_report.name}.docx"
                    inner_name = "".join(c for c in inner_name if c.isalnum() or c in '._- ')
                    zip_file.writestr(inner_name, docx_data)
                    
                except Exception as e:
                    print(f"Ошибка при генерации {doc_type}: {e}")
                    # Продолжаем с другими документами
                    
                finally:
                    # Удаляем временный файл
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)
        
        # Проверяем, что ZIP не пустой
        if zip_buffer.getbuffer().nbytes < 100:
            messages.error(request, 'Ошибка: не удалось сгенерировать документы. Проверьте шаблоны.')
            return redirect('/profile/')
        
        # Формируем имя ZIP файла
        zip_filename = f"Документы_практики_{user_report.familia}_{user_report.name}.zip"
        zip_filename = "".join(c for c in zip_filename if c.isalnum() or c in '._- ')
        
        # Отправляем ZIP файл
        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
        response['Content-Length'] = len(zip_buffer.getvalue())
        
        return response
        
    except Exception as e:
        messages.error(request, f'Ошибка при генерации документов: {str(e)}')
        return redirect('/profile/')