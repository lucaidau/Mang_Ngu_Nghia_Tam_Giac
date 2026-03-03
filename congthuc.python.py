import math 
   def dinh_ly_cos(self):
    v = self.quan_li_doi_tuong
    a, b, c = v.get('a'), v.get('b'), v.get('c')
    A, B, C = v.get('A'), v.get('B'), v.get('C')

    if b and c and A and not a:
        v.set('a', math.sqrt(b*b + c*c - 2*b*c*math.cos(math.radians(A))), "Định lý Cos")
        return True

    if a and c and B and not b:
        v.set('b', math.sqrt(a*a + c*c - 2*a*c*math.cos(math.radians(B))), "Định lý Cos")
        return True

    if a and b and C and not c:
        v.set('c', math.sqrt(a*a + b*b - 2*a*b*math.cos(math.radians(C))), "Định lý Cos")
        return True

def ban_kinh_noi_tiep(self):
    v = self.quan_li_doi_tuong
    S = v.get('S')
    a, b, c = v.get('a'), v.get('b'), v.get('c')

    if S and a and b and c:
        p = (a+b+c)/2
        v.set('r', S/p, "Bán kính nội tiếp")
        return True

    def heron(self):
    v = self.quan_li_doi_tuong
    a, b, c = v.get('a'), v.get('b'), v.get('c')

    if a and b and c and not v.get('S'):
        p = (a+b+c)/2
        S = math.sqrt(p*(p-a)*(p-b)*(p-c))
        v.set('S', S, "Công thức Heron")
        return True
  
    def nua_chu_vi(self):
    v = self.quan_li_doi_tuong
    a, b, c = v.get('a'), v.get('b'), v.get('c')

    if a and b and c and not v.get('p'):
        v.set('p', (a+b+c)/2, "Nửa chu vi")
        return True

    def ban_kinh_ngoai_tiep(self):
    v = self.quan_li_doi_tuong
    a, A = v.get('a'), v.get('A')

    if a and A and not v.get('R'):
        v.set('R', a/(2*math.sin(math.radians(A))), "Bán kính ngoại tiếp")
        return True

    def nhan_dien_vuong(self):
    v = self.quan_li_doi_tuong
    a, b, c = v.get('a'), v.get('b'), v.get('c')

    if a and b and c:
        if abs(a*a - (b*b + c*c)) < 1e-6:
            print("Tam giác vuông")
            return True
