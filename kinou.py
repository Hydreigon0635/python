print('税抜き価格を入力してください')

tax_rate = 0.1
ex_price = int(input())
int_price = int(ex_price * (1 + tax_rate))

print('税込み価格は{}です'.format(int_price))
