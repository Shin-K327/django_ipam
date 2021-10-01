# Django Simple IP Address Manager

djangoの勉強のために製作したIPアドレス管理アプリです  
ネットワークセグメント単位でIPを払い出し、ホストを割り当てられます

今回は、最小の機能のみの実装ですが  
後々DNS用のリソースレコード生成や、仮想基盤サーバやクラウド向けのデプロイコードの書き出し    
等の機能を追加したアプリをDRFベースで新規開発中です

したがって、こちらのアプリはバグ対応中心になる予定です  

## 使い方
通常のdjangoアプリと同様に、
ダウンロード後、settings.pyの必要項目
- データベースの設定
- SECRET_KEYの設定 
 
を実施して頂き、マイグレーション後にサーバを起動してください

## 課題
- 1677万件のInsertが発生するのを避けるため、暫定的にクラスAアドレスも/16からサブネットして使うようになっています
- /16の6.5万件も怪しいので大量のレコード登録に備えてある程度の長さで分割するトランザクションを実装する予定です
