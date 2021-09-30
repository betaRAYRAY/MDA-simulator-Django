from django.shortcuts import redirect, render
from .forms import SequenceForm, PrimerForm, SettingForm
from .input_functions import add_sequences_to_db, add_covid_primers_to_db, add_settings_to_db, update_primer_setting
from .calculations_functions import anneal_primers, calculate_primer_products, calculate_results, create_result_strings
from .models import Sequence, Primer, Setting, AnnealedPrimer, PrimerProduct, ResultString

# Create your views here.
def show_input(request):
    sequence_db = Sequence.objects.all
    primer_db = Primer.objects.all
    primer_count_db = Primer.objects.count
    setting_db = Setting.objects.all

    forms = [SequenceForm(), PrimerForm(),SettingForm()]
 
    if request.method == 'POST':
        # read file
        sequence_file = request.FILES.get('sequence_file', False)
        primer_file = request.FILES.get('primer_file', False)
        add_sequences_to_db([sequence_file, primer_file], True)
        
        # get textarea
        sequence_textarea = request.POST.get('seq_h', False)
        primer_textarea = request.POST.get('pri_h', False)
        add_sequences_to_db([sequence_textarea, primer_textarea], False)

        # check for use of covid primers
        use_covid_primers = request.POST.get('covid', False)
        add_covid_primers_to_db(use_covid_primers)

        # save settings input
        number_of_products = request.POST.get('number_of_products', False)
        number_of_products_EACHONCE = request.POST.get('number_of_products_EACHONCE', False)
        global_termination_probability = request.POST.get('global_termination_probability', False)
        local_termination_probability = request.POST.get('local_termination_probability', False)
        chimerism_model = request.POST.get('chimerism_model', False)
        chimerism_probability = request.POST.get('chimerism_probability', False)
        add_settings_to_db(number_of_products, number_of_products_EACHONCE, global_termination_probability, local_termination_probability, chimerism_model, chimerism_probability)

        # save primer settings
        for primer in primer_db():
            primer_id = str(primer.id)
            active = request.POST.get(primer_id + "checkbox" , False)
            if (active == "isactive"):    # active is string -> convert to Bool
                active = True
            mismatches = request.POST.get(primer_id + "range" , False)
            update_primer_setting(primer_id, active, mismatches)

    if (request.POST.get('start', False)):
        calculate_primer_products()
        calculate_results()
        create_result_strings()
        return redirect('/results')
    else:   
        context = {'sequence':forms[0], 'primer':forms[1], 'setting':forms[2], 'sequence_db':sequence_db, 'primer_db':primer_db, 'primer_count_db':primer_count_db, 'setting_db':setting_db}
        return render(request, 'input.html', context)

def show_results(request):
    annealed_primer = AnnealedPrimer.objects.all()
    primer_product = PrimerProduct.objects.all()
    sequence = Sequence.objects.all()[0].sequence
    result_string = ResultString.objects.all()
    
    return render(request, 'results.html', {'annealed_primer':annealed_primer, 'primer_product':primer_product, 'sequence':sequence, 'result_string':result_string})

def show_howto(request):
    return render(request, 'howto.html', {})
