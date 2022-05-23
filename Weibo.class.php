<?php

/**
 *
 */
class Weibo extends Http {

	private $cookie;

	private $uid;

	function __construct($cookie = '') {

		$this->cookie = $cookie;

	}

	public function getUserWbList($guid, $pn = 1) {

		$url = 'https://m.weibo.cn/api/container/getIndex?containerid=230413' . $guid . '_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page=' . $pn;

		$res = json_decode($this->request($url), true);

		if (isset($res['data']['cards'])) {

			$listw = $res['data']['cards'];

			$index = 1;

			foreach ($listw as $key => $value) {
				if ($value['card_type'] == 9) {
					$index = $key;
					break;
				}
			}

			return array_slice($listw, $index);

		}

		throw new Exception("get list error");

	}

	private function report($guid, $rid) {

		$header = ['Content-Type: application/x-www-form-urlencoded', 'Cookie: ' . $this->cookie, 'Referer: https://service.account.weibo.com/reportspam?rid=' . $rid . '&from=10106&type=1&url=%2Fu%2F' . $guid . '&bottomnav=1&wvr=5', 'User-Agent: ' . HttpHeader::getUserAgent()];

		$data = 'category=8&tag_id=804&url=%2Fu%2F' . $guid . '&type=1&rid=' . $rid . '&uid=' . $this->uid . '&r_uid=' . $guid . '&from=10106&getrid=' . $rid . '&appGet=0&weiboGet=0&blackUser=0&_t=0';
		//var_dump($data);exit();

		return $this->request('https://service.account.weibo.com/aj/reportspam', $data, $header);

	}

	public function reportUid($guid, $time = 4, $pn = 1) {

		try {
			$this->getUid();

			$wlist = $this->getUserWbList($guid, $pn);

			//var_dump(count($wlist));

			$res = '';

			$len = count($wlist);

			//echo $guid . '--' . $len . '<br>';
			//
			$counts = 0;

			$countd = 0;

			for ($i = 0; $i < $len; $i++) {
				try {

					$res = $this->report($guid, $wlist[$i]['mblog']['id']);
					//$title = isset($wlist[$i]['mblog']['raw_text']) ? $wlist[$i]['mblog']['raw_text'] : $wlist[$i]['mblog']['text'];

				} catch (Exception $e) {
					$res = $e->getMessage();
				}

				//echo $res . PHP_EOL;
				//var_dump($res);exit();
				if (stripos($res, 'code":"100002"') !== false) {

					throw new Exception("cookie失效", -1);

				}
				if (stripos($res, 'code":"100000"') !== false) {
					$counts++;
				} else {
					$countd++;
				}
				// if (stripos($res, 'code":"100003"') === false) {

				// 	echo date('m-d H:i:s', time()) . '-' . $guid . '-' . $len . '-' . ($i + 1) . '-' . $res . '<br>';

				// }

				sleep($time);

			}
			echo date('m-d H:i:s', time()) . '-' . $guid . '-' . $len . '-ok-<font color="red" size="5px">' . $counts . '</font>-no-' . $countd . '<br>';

		} catch (Exception $ee) {
			//var_dump($ee->getCode());exit();
			if ($ee->getCode() == -1) {
				sendMail('wbreport故障', '<h1>cookie失效</h1>', '705178580@qq.com');
				throw new Exception("cookie失效", -1);

			}

			echo $ee->getMessage();

		}

	}

	public function block($ruid, $huati) {

		$data = 'mid=&api=http%3A%2F%2Fi.huati.weibo.com%2FSuper_Shield%2FshieldUser%3Foperator%3D1%26user%3D' . $ruid . '%26pageid%3D' . $huati . '%26day%3D1%26sign%3D1836248554%26from%3Dpc';

		$header = ['Content-Type: application/x-www-form-urlencoded', 'Cookie: ' . $this->cookie, 'Referer: ' . 'https://weibo.com/p/' . $huati . '/super_index', 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36', 'X-Requested-With: XMLHttpRequest'];

		return $this->request('https://weibo.com/aj/proxy?ajwvr=6', $data, $header);

	}

	public function sendMsg($suid, $content) {

		$data = 'text=' . $content . '&uid=' . $suid . '&extensions=%7B%7D&is_encoded=0&decodetime=1&source=209678993';

		$header = ['Content-Type: application/x-www-form-urlencoded', 'Cookie: ' . $this->cookie, 'Referer: https://api.weibo.com/chat/', 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'];
		return $this->request('https://api.weibo.com/webim/2/direct_messages/new.json', $data, $header);

	}

	private function getUid() {

		if (empty($this->uid)) {

			$res = json_decode($this->request('https://m.weibo.cn/api/config', '', ['Cookie' => $this->cookie]));
			//var_dump($res);exit;

			if (isset($res->data->login) && $res->data->login == true) {
				$this->uid = $res->data->uid;
				return;
			}

			throw new Exception("get uid error", -1);

		}

	}

	private function request($url, $data = '', $header = []) {

		return $this->setUrl($url)->setHeader($header)->setData($data)->http();

	}

}

?>