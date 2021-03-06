from mdutils.mdutils import MdUtils
import common


def gen_time_metrics_table_markdown(filename, table_name):
    averaged = common.parse_time_metrics_file(filename)

    header = averaged.columns.values.tolist()
    values = averaged.values
    for value in values:
        value[1] = value[1].replace(";", ", ")
        value[1] = value[1].replace("Time threshold", "minTime")
        value[1] = value[1].replace("Objects threshold", "minObj")
    values = values.flatten().tolist()
    header.extend(values)

    columns = len(averaged.columns.values)
    rows = len(header) // columns


    mdFile = MdUtils(file_name=table_name,title=table_name)
    mdFile.new_line()
    mdFile.new_table(columns=columns, rows=rows, text=header, text_align='center')

    mdFile.create_md_file()


def gen_memory_and_network_table_markdown(memory_filename, network_filename, table_name):
    mem_separated = common.separate_measurements(memory_filename)
    net_separated = common.separate_measurements(network_filename)
    assert(len(mem_separated) == len(net_separated))
    measurement_count = len(mem_separated)

    average_memory = 0
    avg_square_mem = 0

    average_net_per_second = 0
    avg_square_net_per_sec = 0

    average_net_packet_size = 0
    avg_square_net_packet_size = 0

    for i in range(measurement_count):
        mem_values = list(map(int, mem_separated[i].split("\n")[:-1]))  # remove separators
        net_values = list(map(int, net_separated[i].split("\n")[:-1]))
        average_memory += mem_values[0]
        avg_square_mem += mem_values[0]**2

        average_net_packet_size += net_values[0]
        avg_square_net_packet_size += net_values[0]**2

        average_net_per_second += net_values[1]
        avg_square_net_per_sec += net_values[1]**2

    avg_square_mem //= measurement_count
    avg_square_net_per_sec //= measurement_count
    avg_square_net_packet_size //= measurement_count

    average_memory //= measurement_count
    average_net_packet_size //= measurement_count
    average_net_per_second //= measurement_count

    mem_deviation = round((avg_square_mem - average_memory**2) ** 0.5, 1)
    net_per_sec_deviation = round((avg_square_net_per_sec - average_net_per_second**2) ** 0.5, 1)
    net_packet_size_deviation = round((avg_square_net_packet_size - average_net_packet_size**2) ** 0.5, 1)



    header = ["Metric", "Value", "Standard deviation",
              "Used memory(Mb)", str(average_memory), mem_deviation,
              "Average network usage(Kb/s)", str(average_net_per_second), net_per_sec_deviation,
              "Average packet size(bytes)", str(average_net_packet_size), net_packet_size_deviation]

    mdFile = MdUtils(file_name=table_name,title=table_name)
    mdFile.new_line()
    mdFile.new_table(columns=3, rows=4, text=header, text_align='center')

    mdFile.create_md_file()




if __name__ == "__main__":
    gen_time_metrics_table_markdown("awtMetrics.csv", "AwtTable")
    gen_time_metrics_table_markdown("createUpdateMetrics.csv", "CreateUpdateTable")
    gen_memory_and_network_table_markdown("memoryMetrics.txt", "networkMetrics.txt", "OtherStats")
