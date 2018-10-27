from label import label

def comment_sanitizer(asm):
    asm = [line[0:line.find('#')].strip() for line in asm]
    return asm

def label_checker(asm):
    data_size_count = 0
    instruction_count = 0
    label_list = []
    dot_data_found = False
    data = True
    text = False
    for line in asm:
        if data:
            if not dot_data_found:
                if ".data" not in line:
                    continue
                else:
                    dot_data_found = True
                    continue
            if ".text" not in line:
                label_name = line[0:line.find(":")].strip()
                location = 0x10000000+(data_size_count)*4;
                new_label = label(label_name, location)
                data_size_count += 1
                label_list.append(new_label)
            else:
                data = False
                text = True
                continue
        elif text:
            if ":" in line:

            
