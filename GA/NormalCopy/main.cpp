#include <iostream>
#include <cstdio>
#include <cstring>
#include <algorithm>
#include <cmath>

using namespace std;
const int MAXN = 30;

struct Point{
    double x,y;
}p[MAXN];
bool vis[MAXN];
inline double sqr(double x){return x * x;}
inline double dist(Point a,Point b){
    return sqrt(sqr(a.x - b.x) + sqr(a.y - b.y));
}
int n;
double ans = 0;

void solve(int rt,int cnt,double res,int init){
    // cout<<"rt = "<<rt<<" cnt = "<<cnt<<" init = "<<init<<endl;
    if(cnt == n + 1 && rt == init){
        ans = min(ans,res);
        return ;
    }
    if(cnt >= n + 1) return ;
    for(int i=1;i<=n;i++){
        if(vis[i] == true) continue;
        vis[i] = true;
        solve(i,cnt + 1,res + dist(p[rt],p[i]),init);
        vis[i] = false;
    }
}
int main(){
    freopen("data.in","r",stdin);
    freopen("data.out","w",stdout);

    scanf("%d",&n);
    for(int i=1;i<=n;i++) {
        scanf("%lf%lf",&p[i].x,&p[i].y);
    }
    
    ans = double(0x3f3f3f3f);
    for(int i=1;i<=n;i++){
        solve(i,1,0.0,i);
    }
    cout<<ans<<endl;
    return 0;
}