#include <bits/stdc++.h>
using namespace std;

#define endl '\n'
// #define int long long

#define watch(...) __f(#__VA_ARGS__, __VA_ARGS__)
template <typename Arg1>
void __f(const char* name, Arg1&& arg1) {
   cerr << name << ": " << arg1 << endl;
}
template <typename Arg1, typename... Args>
void __f(const char* names, Arg1&& arg1, Args&&... args) {
   const char* comma = strchr(names + 1, ',');
   cerr.write(names, comma - names) << ": " << arg1 << " |";
  __f(comma + 1, args...);
}

#define FOR(i, n) for (int i = 0; i < n; ++i)

typedef long long ll;
typedef long double ld;

typedef vector<int> vi;
typedef pair<int, int> pii;

const int INF = 1000000000;
const int MOD = 1000000007; // 998244353

signed main() {
   ios::sync_with_stdio(false);
   cin.tie(nullptr);
   
   return 0;
}
