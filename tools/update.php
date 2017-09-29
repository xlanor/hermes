<?php
include('connection.php');
class updateWallet
{
	private function getjson($url)
	{	
		/*Gets an array from MEW's json*/
		$walleturl = file_get_contents($url);
		$wallet_json = json_encode($walleturl);
		$wallet_decoded_json = json_decode($walleturl,true);
		return $wallet_decoded_json;
	}
	private function updatedb($json_array,$dbh)
	{
		foreach($json_array as $jsonarray)
		{
			/*Lets see if the json string contains any symbols that we already have,*/
			$symbol = $jsonarray['symbol'];
			$address =$jsonarray['address'];
			$check_symbol_q = "SELECT * FROM cmc_ticker WHERE ticker_symbol = :symbol";
			$check_symbol_x = $dbh->prepare($check_symbol_q);
			$check_symbol_x->bindValue(':symbol',$symbol);
			$check_symbol_x->execute();
			/*if the symbol is present, we just need to add the address to it*/
			if($check_symbol_x->rowCount() > 0)
			{
				$add_address_q = "UPDATE cmc_ticker SET ticker_address = :address,token_type = 1 WHERE ticker_symbol = :symbol";
				$add_address_x = $dbh->prepare($add_address_q);
				$add_address_x->bindValue(':address',$address);
				$add_address_x->bindValue(':symbol',$symbol);
				$add_address_x->execute();
				echo $symbol.'\'s address has been updated in the database'.PHP_EOL;
			}
			else
			{
				/*if it's not present, we need to get the name and then insert it into our db along with the other information*/
				echo $symbol.' not found in database'.PHP_EOL;
				echo 'Searching Ethplorer for more information...'.PHP_EOL;
				$ethplorerurl = "https://api.ethplorer.io/getTokenInfo/".$address."?apiKey=freekey";
				$ch = curl_init();
				curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
				curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
				curl_setopt($ch, CURLOPT_URL, $ethplorerurl);
				$result = curl_exec($ch);
				curl_close($ch);

				$obj = json_decode($result,true);
				if(array_key_exists("error", $obj))
				{
					/*if ETHplorer doesnt have it, we take our thumb and we suck it really hard*/
					echo $symbol.' was not found in Ethplorer either'.PHP_EOL;
				}
				else
				{
					$name = $obj['name'];
					$add_address_q = "INSERT INTO cmc_ticker VALUES(NULL,:id,:symbol,:add,1)";
					$add_address_x = $dbh->prepare($add_address_q);
					$add_address_x->bindValue(':id',$name);
					$add_address_x->bindValue(':add',$address);
					$add_address_x->bindValue(':symbol',$symbol);
					$add_address_x->execute();
					echo $symbol.'\'s record has been inserted in the database'.PHP_EOL;

				}
			}
		}
	}
	public function fire($url,$dbh)
	{
		$json = $this->getjson($url);
		$this->updatedb($json,$dbh);
	}

}
$url = 'https://raw.githubusercontent.com/kvhnuke/etherwallet/mercury/app/scripts/tokens/ethTokens.json';
$updateWallet = new updateWallet;
$updateWallet->fire($url,$dbh);
?>