<?php

/**
 *
 */
class Http {

	private $url;
	private $data;
	private $ip;
	private $header;

	function __construct($url = '', $header = [], $data = '') {

		$this->url = $url;

		$this->data = $data;

		$this->header = (new HttpHeader($header))->getHeader();
	}

	public function setUrl($url) {
		$this->url = $url;

		return $this;
	}

	public function setHeader($header = []) {
		$this->header = (new HttpHeader($header))->getHeader();

		return $this;
	}

	public function setData($data = '') {
		$this->data = $data;
		return $this;
	}

	public function setIp($ip) {
		$this->ip = $ip;
		return $this;

	}
	public function http() {

		$curl = curl_init();
		curl_setopt($curl, CURLOPT_URL, $this->url);
		curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1); // 抓取结果直接返回（如果为0，则直接输出内容到页面）
		curl_setopt($curl, CURLOPT_HEADER, 0);
		curl_setopt($curl, CURLOPT_HTTPHEADER, $this->header);

		curl_setopt($curl, CURLOPT_TIMEOUT, 15);
		if (!empty($this->data)) {
			if (is_array($this->data)) {
				$this->data = http_build_query($this->data);
			}
			curl_setopt($curl, CURLOPT_POST, 1);
			curl_setopt($curl, CURLOPT_POSTFIELDS, $this->data);
			//var_dump($this->data);die;
		}
		if (!empty($this->ip)) {
			$iparr = explode(':', $this->ip);
			curl_setopt($curl, CURLOPT_PROXY, $iparr[0]);

			curl_setopt($curl, CURLOPT_PROXYPORT, $iparr[1]);

		}
		$content = curl_exec($curl); //执行并存储结果

		if ($content === false) {

			throw new Exception(curl_error($curl));
		}

		curl_close($curl);

		return $content;

	}
}

?>