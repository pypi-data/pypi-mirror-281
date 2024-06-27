from qg_toolkit.tools.yescaptcha import YesCaptcha


class A:
    client_key = "c14f6a8da73559b4fbfd2de46eb7a4237c25cd15521"
    website_key = "0x4AAAAAAAaHm6FnzyhhmePw"
    website_url = "https://pioneer.particle.network/zh-CN/point"
    def __init__(self):
        self.yes_captcha = YesCaptcha(self.client_key, self.website_key, self.website_url, task_type="TurnstileTaskProxyless")

    def get_solution(self):
        self.yes_captcha.get_solution()


if __name__ == "__main__":
    A().get_solution()