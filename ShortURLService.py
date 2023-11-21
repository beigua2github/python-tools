import mmh3
import string


class ShortURLService:
    def __init__(self):
        self.url_mapping = {}

    def generate_short_url(self, original_url):
        # 使用 MurmurHash 算法生成短网址
        hash_value = mmh3.hash(original_url)
        short_url = self.to_base62(abs(hash_value))

        # 在数据库中查找是否存在相同的短网址
        if short_url not in self.url_mapping:
            # 如果不存在相同的短网址，将其存储到数据库
            self.url_mapping[short_url] = original_url
            return short_url
        else:
            # 如果存在相同的短网址，处理冲突
            duplicated_suffix = "[DUPLICATED]"
            new_original_url = original_url + duplicated_suffix

            # 再次生成哈希值
            new_hash_value = mmh3.hash(new_original_url)
            new_short_url = self.to_base62(abs(new_hash_value))

            # 存储新的短网址到数据库
            self.url_mapping[new_short_url] = new_original_url
            return new_short_url

    def get_original_url(self, short_url):
        # 通过短网址在数据库中查找对应的原始网址
        if short_url in self.url_mapping:
            original_url = self.url_mapping[short_url]

            # 检查是否存在特殊字符
            if "[DUPLICATED]" in original_url:
                # 去掉特殊字符
                original_url = original_url.replace("[DUPLICATED]", "")

            return original_url
        else:
            return None

    def to_base62(self, num):
        characters = string.digits + string.ascii_uppercase + string.ascii_lowercase
        base62 = ""

        while num > 0:
            remainder = num % 62
            base62 = characters[remainder] + base62
            num //= 62

        return base62 if base62 else "0"


url_service = ShortURLService()
original_url = "https://example.com"
short_url = url_service.generate_short_url(original_url)
SHOR_URL_PREFIX = 'http://t.cn'
print(f"Original URL: {original_url}")
print(f"Short URL: {SHOR_URL_PREFIX}/{short_url}")

retrieved_url = url_service.get_original_url(short_url)
print(f"Retrieved URL: {retrieved_url}")
