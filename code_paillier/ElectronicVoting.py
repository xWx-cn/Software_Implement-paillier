# -*- coding: utf-8 -*-
from crypto.paillier import keygen, encrypt, decrypt

def get_valid_input(prompt, validator, error_message):
    """ 获取并校验用户输入 """
    while True:
        try:
            value = int(input(prompt))
            if validator(value):
                return value
            else:
                print(error_message)
        except ValueError:
            print("无效输入，请输入一个整数！")
def print_round_result(round_number, candidates_votes):
    """ 打印每一轮的投票结果 """
    print(f"-------------------result of {round_number + 1} round -------------------")
    for idx, vote in enumerate(candidates_votes):
        print(f"the vote of candidate {idx + 1} is: {vote}\n")
def print_final_results(candidates_votes, private_key, public_key):
    """ 打印最终投票结果 """
    print("---------------Final Results---------------")
    for idx, encrypted_vote in enumerate(candidates_votes):
        decrypted_vote = decrypt(private_key, public_key, encrypted_vote)
        print(f"the final vote of candidate {idx + 1} is: {decrypted_vote}")

def main():
    # 生成密钥对
    try:
        public_key, private_key = keygen()
    except Exception as e:
        print(f"密钥生成失败：{e}")
        return
    print(f"public key: {public_key}")
    
    # 获取票数和候选人数量
    num_votes = get_valid_input("please set the number of votes:", lambda x: x > 0, "请输入一个大于0的整数！")
    num_candidates = get_valid_input("please set the number of candidates:", lambda x: x > 0, "请输入一个大于0的整数！")
    
    if num_candidates == 0:
        print("没有候选人，程序退出。")
        return
    
    # 初始化候选人票数列表，加密后的0作为初始值
    candidates_votes = [encrypt(public_key, 0) for _ in range(num_candidates)]
    round_votes = [encrypt(public_key, 0) for _ in range(num_candidates)]

    # 开始投票
    for i in range(num_votes):
        print(f"-------------------the {i + 1} round vote-------------------")
        round_votes = [encrypt(public_key, 0) for _ in range(num_candidates)]
        round_valid = False
        
        while not round_valid:
            for j in range(num_candidates):
                while True:
                    try:
                        print(f"please vote for candidate {j + 1} (0 or 1):")
                        vote_value = get_valid_input("", lambda x: x in [0, 1], "请输入0或1！")
                        encrypted_vote = encrypt(public_key, vote_value)
                        round_votes[j] = encrypted_vote  % (public_key[0]**2)
                        candidates_votes[j] = (encrypted_vote * candidates_votes[j]) % (public_key[0]**2)
                        break  # 输入有效，跳出循环
                    except Exception as e:
                        print(f"加密失败：{e}")
                 # 检查候选人是否得一票
                if decrypt(private_key, public_key, round_votes[j]) > 0:
                    round_valid = True
                     # 一旦获得一票，其他候选者的票数在本轮设为0
                    for j in range(num_candidates):
                        if decrypt(private_key, public_key, round_votes[j]) == 0:
                            candidates_votes[j] = ( round_votes[j] * candidates_votes[j]) % (public_key[0]**2)
                    print("---------------this round is over---------------\n")
                    break

            # 检查是否有至少一个候选人获得一票
            if any(decrypt(private_key, public_key, vote) > 0 for vote in round_votes):
                round_valid = True
            else:
                print("至少有一个候选人必须获得一票，请重新进行本轮投票。")
        
        # 打印本轮投票结果
        print_round_result(i, candidates_votes)
    
    # 解密并打印最终结果
    try:
        print_final_results(candidates_votes, private_key, public_key)
    except Exception as e:
        print(f"解密失败：{e}")


if __name__ == '__main__':
    main()