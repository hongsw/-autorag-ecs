import os
import sys
import yaml

def replace_profile_name(yaml_file, env_var_name):
    # YAML 파일 읽기
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)
    
    # 환경 변수에서 값 가져오기
    profile_name = os.environ.get(env_var_name)
    
    if profile_name is None:
        print(f"오류: 환경 변수 {env_var_name}가 설정되지 않았습니다.")
        sys.exit(1)
    
    # node_lines 리스트를 순회하며 profile_name 대체
    for node_line in data.get('node_lines', []):
        for node in node_line.get('nodes', []):
            for module in node.get('modules', []):
                if module.get('module_type') == 'llama_index_llm' and 'profile_name' in module:
                    module['profile_name'] = profile_name
                    print(f"프로필 이름이 {profile_name}으로 대체되었습니다.")

    # 수정된 YAML 파일 쓰기
    with open(yaml_file, 'w') as file:
        yaml.dump(data, file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("사용법: python script.py <yaml_파일> <환경_변수_이름>")
        sys.exit(1)
    
    yaml_file = sys.argv[1]
    env_var_name = sys.argv[2]
    
    replace_profile_name(yaml_file, env_var_name)
    print(f"YAML 파일이 성공적으로 업데이트되었습니다.")