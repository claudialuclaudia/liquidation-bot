import cosmosDb


def main():
    file1 = open('past_borrows_from_tenderly.txt', 'r')
    Lines = file1.readlines()
    
    next_line_is_user_address = False
    for line in Lines:
        if line.strip() == 'Success':
            next_line_is_user_address = True
        elif next_line_is_user_address:
            print(line.strip())
            next_line_is_user_address = False
        
    cosmosDb.insert_()
    
    file1.close()

main()