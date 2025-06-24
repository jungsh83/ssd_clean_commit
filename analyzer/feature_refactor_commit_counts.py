import subprocess


def count_commits(keyword):
    try:
        result = subprocess.run(
            ['powershell', '-Command', f'git log --oneline --grep "{keyword}" -i | Measure-Object -Line'],
            capture_output=True, text=True, check=True
        )

        # 결과에서 "Lines : <숫자>" 라인을 찾기
        for line in result.stdout.splitlines():
            if "Lines" in line:
                count = int(line.split(":")[-1].strip())
                return count
    except subprocess.CalledProcessError as e:
        print(f"Error running git command for keyword '{keyword}':", e)
        return 0


if __name__ == "__main__":
    feature_count = count_commits("feature")
    refactor_count = count_commits("refactor")
