from .forms import AnnealedPrimerForm, PrimerProductForm, ResultProductForm, ChimericResultProductForm, ResultStringForm
from .models import Sequence, Primer, Setting, AnnealedPrimer, PrimerProduct, ResultProduct, ChimericResultProduct, ResultString
from random import *

def calculate_primer_products():
    anneal_primers()
    annealed_primers = AnnealedPrimer.objects.all()
    forward_primers = []
    reverse_primers = []
    deleted = False
    for item in annealed_primers:
        if item.primer.direction:
            forward_primers.append(item)
        else:
            reverse_primers.append(item)
    
    for forward_primer in forward_primers:
        for reverse_primer in reverse_primers:
            if forward_primer.end < reverse_primer.start:
                # save product
                data = {'forward_primer': forward_primer, 'reverse_primer': reverse_primer}
                form = PrimerProductForm(data)
                if form.is_valid():
                    if not deleted:
                        deleted = True
                        PrimerProduct.objects.all().delete()
                    form.save()
                

def anneal_primers():
    sequence = Sequence.objects.all()[0].sequence
    sequence_length = len(sequence)
    primer_set = Primer.objects.filter(active=True)
    deleted = False
    for primer in primer_set:
        primer_sequence = primer.sequence
        primer_length = len(primer_sequence)
        mismatch_score = primer.mismatch_score

        for j in range(sequence_length - primer_length + 1):
            if (hamming_distance(primer_sequence, sequence[j:j+primer_length])) <= mismatch_score:
                start = j
                end = j + primer_length - 1
                data = {'primer': primer, 'start': start, 'end': end}
                form = AnnealedPrimerForm(data)
                if form.is_valid():
                    if not deleted:
                        deleted = True
                        AnnealedPrimer.objects.all().delete()
                    form.save()

def hamming_distance(s1, s2): # string 1 and 2
	if len(s1) != len(s2):
		print("error: sequences for hamming distance have to be of same length.")
	else:
		distance = 0
		for i in range(0,len(s1)):
			if s1[i] != s2[i]:
				distance += 1
		return distance    

def calculate_results():
    ResultProduct.objects.all().delete()
    ChimericResultProduct.objects.all().delete()

    settings = Setting.objects.all()[0]
    primer_products = PrimerProduct.objects.all()
    used_products = []
    if (settings.number_of_products_EACHONCE):
        # each product used once
        used_products = primer_products
    else:
        # use random set of products in given amount
        for i in range(settings.number_of_products):
            if (len(primer_products) > 0):
                used_products.append(choice(primer_products))
    
    for item in used_products:
        if (check_odds(settings.chimerism_probability) and settings.chimerism_model != "no_model"):
            # chimerism model applied
            data = {}
            if (settings.chimerism_model == "A"):
                data = chimerism_A(item)
            elif (settings.chimerism_model == "B"):
                data = chimerism_B(item)
            elif (settings.chimerism_model == "C"):
                data = chimerism_C(item)

            data['primer_product_1'] = item
            form = ChimericResultProductForm(data)
            if form.is_valid():
                form.save()

        elif (check_odds(settings.global_termination_probability)):
            # sequence terminated early
            end_fw_primer = item.forward_primer.end
            start_rv_primer = item.reverse_primer.start
            non_primer_sequence_length = start_rv_primer - end_fw_primer - 1
            beginning = check_odds(50) # start from forward or reverse primer?
            
            breakpoint = False
            i = 0
            while (i < non_primer_sequence_length) and (breakpoint == False):
                if (check_odds(settings.local_termination_probability)):
                    breakpoint = i
                i += 1
            
            break_position = ""
            data = {}
            if (breakpoint):
                if (beginning):
                    break_position = end_fw_primer + breakpoint + 1
                else:
                    break_position = start_rv_primer - breakpoint + 1
            
                data = {'primer_product': item, 'stop': break_position, 'direction': beginning}
            else:
                data = {'primer_product': item, 'stop': -1, 'direction': True}
                
            form = ResultProductForm(data)
            if form.is_valid():
                form.save()

        else:
            # whole sequence used
            data = {'primer_product': item, 'stop': -1, 'direction': True}
            form = ResultProductForm(data)
            if form.is_valid():
                form.save()

def check_odds(percentage):
    p = percentage / 100
    random_odds = random()

    if (random_odds > p):
        return False
    else:
        return True

# combine random primer products
def chimerism_A(primer_product_1):
    primer_product_2 = choice(PrimerProduct.objects.all())
    proportion = random()
    between_length_1 = (primer_product_1.reverse_primer.start - primer_product_1.forward_primer.end) - 1
    between_length_2 = (primer_product_2.reverse_primer.start - primer_product_2.forward_primer.end) - 1
    
    stop1 = primer_product_1.forward_primer.end + (proportion * between_length_1) +1    # +/-1: stop 1 lies outside of used sequence
    stop2 = primer_product_2.reverse_primer.start - ((1-proportion) * between_length_2) -1

    return({'primer_product_2': primer_product_2, 'stop_1': round(stop1), 'stop_2': round(stop2)})

# anneal stopped sequence 1 on most fitting position, complete using primer product 2
def chimerism_B(primer_product_1):
    primer_products = PrimerProduct.objects.all()
    sequence = Sequence.objects.all()[0].sequence

    proportion = random()
    between_length_1 = (primer_product_1.reverse_primer.start - primer_product_1.forward_primer.end) - 1
    stop_1 = round(primer_product_1.forward_primer.end + (proportion * between_length_1) +1)    # +/-1: stop 1 lies outside of used sequence

    product_sequence = primer_product_1.forward_primer.primer.sequence + sequence[primer_product_1.forward_primer.start:stop_1]

    mismatches = float('inf')
    used_product = primer_products[0]
    for item in primer_products:
        if ((item.reverse_primer.start - item.forward_primer.start) > len(product_sequence)): # primerproduct 2 has to be longer than matchin sequence from pp1
            mm_fit = hamming_distance(product_sequence, sequence[item.forward_primer.start:item.forward_primer.start+len(product_sequence)])
            if mm_fit < mismatches:
                used_product = item
                mismatches = mm_fit

    stop_2 = used_product.forward_primer.start + len(product_sequence) + 1

    return({'primer_product_2': used_product, 'stop_1': stop_1, 'stop_2': stop_2})

# use primerproduct 2 as a primerproduct lying in proximity to product 1, lesser chance of combination for bigger distance
def chimerism_C(primer_product_1):
    primer_products = PrimerProduct.objects.all()
    sequence = Sequence.objects.all()[0].sequence

    proportion = random()
    between_length_1 = (primer_product_1.reverse_primer.start - primer_product_1.forward_primer.end) - 1
    stop_1 = round(primer_product_1.forward_primer.end + (proportion * between_length_1) +1)    # +/-1: stop 1 lies outside of used sequence

    product_sequence = primer_product_1.forward_primer.primer.sequence + sequence[primer_product_1.forward_primer.start:stop_1]

    distance_sum = 0
    distances = []
    for item in primer_products:
        distance = abs(item.forward_primer.start - primer_product_1.forward_primer.start) # distance between products
        if (distance != 0): # no division by zero, no use of already used primer product
            distance = 1/distance
        distance_sum = distance_sum + distance
        distances.append(distance)
    
    decision_num = uniform(0,distance_sum)
    count = 0
    i = 0
    while (decision_num > count and i < len(distances)):
        count = count + distances[i]
        i = i + 1
    
    used_product = primer_products[i]

    stop_2 = used_product.forward_primer.start + len(product_sequence) + 1

    return({'primer_product_2': used_product, 'stop_1': stop_1, 'stop_2': stop_2})

def create_result_strings():
    ResultString.objects.all().delete()
    sequence = Sequence.objects.all()[0].sequence
    result_products = ResultProduct.objects.all()
    chimeric_result_products = ChimericResultProduct.objects.all()

    result_string = ""
    for item in result_products:
        forward_primer = "<div style='display:inline; color:#0099ff'>"
        reverse_primer = "<div style='display:inline; color:#ff0000'>"
        between_sequence = ""

        # make foward primer string
        sub_sequence = sequence[item.primer_product.forward_primer.start:item.primer_product.forward_primer.end+1]
        fw_primer_sequence = item.primer_product.forward_primer.primer.sequence
        for i in range(len(sub_sequence)):
            if (sub_sequence[i] == fw_primer_sequence[i]):
                forward_primer = forward_primer + fw_primer_sequence[i]
            else:
                forward_primer = forward_primer + "<b style='color:darkblue'>" + fw_primer_sequence[i] + "</b>"
        forward_primer = forward_primer + "</div>"

        # make reverse primer string 
        sub_sequence = sequence[item.primer_product.reverse_primer.start:item.primer_product.reverse_primer.end+1]
        rv_primer_sequence = item.primer_product.reverse_primer.primer.sequence
        for i in range(len(sub_sequence)):
            if (sub_sequence[i] == rv_primer_sequence[i]):
                reverse_primer = reverse_primer + rv_primer_sequence[i]
            else:
                reverse_primer = reverse_primer + "<b style='color:darkred'>" + rv_primer_sequence[i] + "</b>"
        reverse_primer = reverse_primer + "</div>" 

        start_num = ""
        end_num = ""   
        global_start_num = "<div style='display:inline; color:dimgrey; font-size: 15px;'>" + str(item.primer_product.forward_primer.start) + "&nbsp;</div>"
        global_end_num = "<div style='display:inline; color:dimgrey; font-size: 15px;'>&nbsp;" + str(item.primer_product.reverse_primer.end) + "</div>"
        if (item.stop == -1):   # whole sequence
            # make in-between-string
            start_num = str(item.primer_product.forward_primer.end +1)
            end_num = str(item.primer_product.reverse_primer.start -1)
        elif (item.direction):  # stopped sequence, forward
            start_num = str(item.primer_product.forward_primer.end +1)
            end_num = str(item.stop) + "<b style='font-size: 20px; color:black;'>&nbsp;&#10650;</b>"   # add zigzag
        else:                   # stopped sequence, backward
            start_num = "<b style='font-size: 20px; color:black;'>&#10713;&nbsp;</b>" + str(item.stop) # add zigzag
            end_num = str(item.primer_product.reverse_primer.start -1)
        
        between_sequence = "<div style='display:inline; color:dimgrey; font-size: 15px;'>&nbsp;" + start_num + "&nbsp;-&nbsp;" + end_num + "&nbsp;</div>"
        
        if (item.stop == -1):   # whole sequence
            result_string = global_start_num + forward_primer + between_sequence + reverse_primer + global_end_num + "<br>"
        elif (item.direction):  # stopped sequence, forward
            result_string = global_start_num + forward_primer + between_sequence + "<br>"
        else:                   # stopped sequence, backward
            result_string = between_sequence + reverse_primer + global_end_num + "<br>"

        data = {'product_string':result_string}
        form = ResultStringForm(data)
        if form.is_valid():
            form.save()    

    for item in chimeric_result_products:
        forward_primer = "<div style='display:inline; color:#0099ff'>"
        reverse_primer = "<div style='display:inline; color:#ff0000'>"

        # make foward primer string (forward primer of primer product 1)
        sub_sequence = sequence[item.primer_product_1.forward_primer.start:item.primer_product_1.forward_primer.end+1]
        fw_primer_sequence = item.primer_product_1.forward_primer.primer.sequence
        for i in range(len(sub_sequence)):
            if (sub_sequence[i] == fw_primer_sequence[i]):
                forward_primer = forward_primer + fw_primer_sequence[i]
            else:
                forward_primer = forward_primer + "<b style='color:darkblue'>" + fw_primer_sequence[i] + "</b>"
        forward_primer = forward_primer + "</div>"

        # make reverse primer string 
        sub_sequence = sequence[item.primer_product_2.reverse_primer.start:item.primer_product_2.reverse_primer.end+1]
        rv_primer_sequence = item.primer_product_2.reverse_primer.primer.sequence
        for i in range(len(sub_sequence)):
            if (sub_sequence[i] == rv_primer_sequence[i]):
                reverse_primer = reverse_primer + rv_primer_sequence[i]
            else:
                reverse_primer = reverse_primer + "<b style='color:darkred'>" + rv_primer_sequence[i] + "</b>"
        reverse_primer = reverse_primer + "</div>" 

        # start and end of in between sequences
        start_num_1 = str(item.primer_product_1.forward_primer.end +1)
        end_num_1 = str(item.stop_1)
        start_num_2 = str(item.stop_2)   
        end_num_2 = str(item.primer_product_2.reverse_primer.start -1)

        # start and end of whole product
        global_start_num = "<div style='display:inline; color:dimgrey; font-size: 15px;'>" + str(item.primer_product_1.forward_primer.start) + "&nbsp;</div>"
        global_end_num = "<div style='display:inline; color:dimgrey; font-size: 15px;'>&nbsp;" + str(item.primer_product_2.reverse_primer.end) + "</div>"
        
        between_sequence_1 = "<div style='display:inline; color:dimgrey; font-size: 15px;'>&nbsp;" + start_num_1 + "&nbsp;-&nbsp;" + end_num_1 + "&nbsp;</div>"
        between_sequence_2 = "<div style='display:inline; color:dimgrey; font-size: 15px;'>&nbsp;" + start_num_2 + "&nbsp;-&nbsp;" + end_num_2 + "&nbsp;</div>"
        
        start_break_zigzag = "<b style='font-size: 20px; color:black;'>&#10714;&nbsp;</b>"
        end_break_zigzag = "<b style='font-size: 20px; color:black;'>&#10715;&nbsp;</b>"

        result_string = global_start_num + forward_primer + between_sequence_1 + start_break_zigzag + end_break_zigzag + between_sequence_2 + reverse_primer + global_end_num + "<br>"

        data = {'product_string':result_string}
        form = ResultStringForm(data)
        if form.is_valid():
            form.save()  