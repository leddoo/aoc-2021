inpt = """220D69802BE00A0803711E1441B1006E39C318A12730C200DCE66D2CCE360FA0055652CD32966E3004677EDF600B0803B1361741510076254138D8A00E4FFF3E3393ABE4FC7AC10410010799D2A4430003764DBE281802F3102CA00D4840198430EE0E00021D04E3F41F84AE0154DFDE65A17CCBFAFA14ADA56854FE5E3FD5BCC53B0D2598027A00848C63F2B918C7E513DEC3290051B3867E009CCC5FE46BD520007FE5E8AD344B37583D0803E40085475887144C01A8C10FE2B9803B0720D45A3004652FD8FA05F80122CAF91E5F50E66BEF8AB000BB0F4802039C20917B920B9221200ABF0017B9C92CCDC76BD3A8C4012CCB13CB22CDB243E9C3D2002067440400D9BE62DAC4D2DC0249BF76B6F72BE459B279F759AE7BE42E0058801CC059B08018A0070012CEC045BA01006C03A8000D46C02FA000A8EA007200800E00618018E00410034220061801D36BF178C01796FC52B4017100763547E86000084C7E8910AC0027E9B029FE2F4952F96D81B34C8400C24AA8CDAF4F1E98027C00FACDE3BA86982570D13AA640195CD67B046F004662711E989C468C01F1007A10C4C8320008742287117C401A8C715A3FC2C8EB3777540048272DFE7DE1C0149AC8BC9E79D63200B674013978E8BE5E3A2E9AA3CCDD538C01193CFAB0A146006AA00087C3E88B130401D8E304A239802F39FAC922C0169EA3248DF2D600247C89BCDFE9CA7FFD8BB49686236C9FF9795D80C0139BEC4D6C017978CF78C5EB981FCE7D4D801FA9FB63B14789534584010B5802F3467346D2C1D1E080355B00424FC99290C7E5D729586504803A2D005E677F868C271AA479CEEB131592EE5450043A932697E6A92C6E164991EFC4268F25A294600B5002A3393B31CC834B972804D2F3A4FD72B928E59219C9C771EC3DC89D1802135C9806802729694A6E723FD6134C0129A019E600"""
expected_version_sum = None
expected_value = None

if 0:
    inpt = """8A004A801A8002F478"""
    expected_version_sum = 16

if 0:
    inpt = """620080001611562C8802118E34"""
    expected_version_sum = 12

if 0:
    inpt = """C0015000016115A2E0802F182340"""
    expected_version_sum = 23

if 0:
    inpt = """A0016C880162017C3686B18A3D4780"""
    expected_version_sum = 31


if 0:
    inpt = """C200B40A82"""
    expected_value = 3

if 0:
    inpt = """04005AC33890"""
    expected_value = 54

if 0:
    inpt = """880086C3E88112"""
    expected_value = 7

if 0:
    inpt = """CE00C43D881120"""
    expected_value = 9

if 0:
    inpt = """D8005AC2A8F0"""
    expected_value = 1

if 0:
    inpt = """F600BC2D8F"""
    expected_value = 0

if 0:
    inpt = """9C005AC2F8F0"""
    expected_value = 0

if 0:
    inpt = """9C0141080250320F1802104A08"""
    expected_value = 1




def hex_to_bin(a):
    a = int(a, 16)

    if a == 0:
        return "0000"

    result = ""
    while a != 0:
        result += str(a % 2)
        a //= 2

    result = "".join(reversed(result))
    result = result.rjust(4, "0")
    return result

def get_bits(string):
    return "".join([ hex_to_bin(char) for char in string ])

assert get_bits("38006F45291200") == "00111000000000000110111101000101001010010001001000000000"


bits = get_bits(inpt)

version_sum = 0

def parse(bits):
    version = int(bits[0:3], 2)
    type_id = int(bits[3:6], 2)
    bits    = bits[6:]

    global version_sum
    version_sum += version

    consumed = 6

    value = None

    if type_id == 4:
        #print("literal")
        value = ""

        was_last = False
        while was_last == False:
            if bits[0] == "0":
                was_last = True

            value += bits[1:5]

            bits = bits[5:]
            consumed += 5

        value = int(value, 2)

        print("literal", value)

    else:
        sub_values = []

        #print("operator")
        if bits[0] == "0":
            total_length = int(bits[1:16], 2)
            bits = bits[16:]
            consumed += 16

            #print(f"with {total_length} bits")

            cursor = 0
            while cursor < total_length:
                length, sub_value = parse(bits)
                sub_values.append(sub_value)
                bits = bits[length:]
                cursor += length
            assert cursor == total_length

            consumed += total_length

        else:
            count = int(bits[1:12], 2)
            bits = bits[12:]
            consumed += 12

            #print(f"with {count} sub-packets")

            for _ in range(count):
                length, sub_value = parse(bits)
                sub_values.append(sub_value)
                bits = bits[length:]
                consumed += length

        if type_id == 0:
            print("sum", end=" ")
            value = sum(sub_values)
        elif type_id == 1:
            print("product", end=" ")
            value = 1
            for v in sub_values:
                value *= v
        elif type_id == 2:
            print("min", end=" ")
            value = min(sub_values)
        elif type_id == 3:
            print("max", end=" ")
            value = max(sub_values)
        elif type_id == 5:
            print(">", end=" ")
            assert len(sub_values) == 2
            value = int(sub_values[0] > sub_values[1])
        elif type_id == 6:
            print("<", end=" ")
            assert len(sub_values) == 2
            value = int(sub_values[0] < sub_values[1])
        elif type_id == 7:
            print("=", end=" ")
            assert len(sub_values) == 2
            value = int(sub_values[0] == sub_values[1])
        else:
            assert False

        print(sub_values, value)

    assert value is not None

    return (consumed, value)


version_sum = 0
print(parse(bits), len(bits), version_sum, expected_version_sum, expected_value)

