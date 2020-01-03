def retry_get(self, url, headers, count):
        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
            if response.status_code == 200:
                return response
            raise Exception
        except:
            if count < 10:
                # if self.judge_stop():
                #     return
                response = self.retry_get(url, headers, count + 1)
                return response
            else:
                return None