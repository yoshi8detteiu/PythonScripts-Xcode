**TBD**

# PythonScripts-Xcode
Python scripts for Xcode project.<br>
ちゃんと検証はしていないので、使用は自己責任で :pray:

## Usage
Anaconda Python 3.7を導入して、Xcodeプロジェクト直下のディレクトリで実行するだけ

## attributedString_finder.py
Xcode11で、attributedStringが明朝体になる現象が発生した。<br>
原因の一つに改行文字が、指定されたフォント以外になることがわかったので、それを見つけるためのScript。<br>
(他にも原因があるらしいので、これだけですべての明朝体バグを見つけられるわけでは無い)<br>

## color_exchanger.py
storyboardとxib内で、AssetCatalogで宣言していない色を見つけて<br>
AssetCatalogで宣言されている近しい色と置換する。<br>
色の近さは、ユークリッド距離で算出しているので精度はそこまで良くない。<br>
またsRGBにしか対応していないので、DisplayP3とかの色空間を使っているプロジェクトでは使えない。<br>

## color_finder.py
storyboardとxib内で、AssetCatalogで宣言していない色を見つけるだけ。<br>
CIとかでLint的な使い方を想定して作った。<br>

## deprecated_finder.py
storyboardやxib内でdeprecatedなクラスへの参照があり、それがクラッシュすることがあったので<br>
それらを探すためのScriptを書いた。<br>
ただし検索してるのは、それっぽいUIKit系のdeprecatedを何個か拾ってきただけなので注意。<br>
