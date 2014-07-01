#include<iostream>
#include<cstdlib>
#include<cstring>
#include<ctime>
#include<vector>
#include<map>

using namespace std;

const int maxm = 1000010;
const int maxn = 10010;

int n, q;
vector<int> termPostingList[maxm];

// Load pins and objects.
void loadData() {
    cin >> n;
    for (int i = 0; i < n; ++i) {
        int terms, t;
        cin >> terms;
        for (int j = 0; j < terms; ++j) {
            cin >> t;
            termPostingList[t].push_back(i);
        }
    }
}

int docset[maxn];
string queryStr;

// A function that helps you split string by delimiter.
vector<string> split(string query, string delimiter) {
    vector<string> tokens;
    int start = 0, end = 0;
    while ((end = query.find(delimiter, start)) != string::npos) {
        tokens.push_back(query.substr(start, end - start));
        start = end + delimiter.size();
    }
    tokens.push_back(query.substr(start));
    return tokens;
}

// Parse a search query.
vector< vector<int> > parse(string queryStr) {
    vector<string> tokens = split(queryStr, " and ");
    vector< vector<int> > query;
    for (int i = 0; i < tokens.size(); ++i) {
        vector<int> clause;
        if (tokens[i][0] == '(') {
            vector<string> terms = split(tokens[i].substr(1, tokens[i].size() - 2), " or ");
            for (int j = 0; j < terms.size(); ++j) {
                clause.push_back(atoi(terms[j].c_str()));
            }
        } else
            clause.push_back(atoi(tokens[i].c_str()));
        query.push_back(clause);
    }
    return query;
}

// Load queries and output answers.
void work() {
    cin >> q;
    getline(cin, queryStr);
    for (int i = 0; i < q; ++i) {
        memset(docset, 0, sizeof(docset));
        getline(cin, queryStr);
    
        vector< vector<int> > query = parse(queryStr);
        for (int j = 0; j < query.size(); ++j) {
            for (int t = 0; t < query[j].size(); ++t) {
                int term = query[j][t];
                for (int index = 0; index < termPostingList[term].size(); ++index)
                    if (docset[termPostingList[term][index]] == j) {
                        docset[termPostingList[term][index]] = j + 1;
                    }
            }
        }
        
        int ans = 0;
        for (int j = 0; j < n; ++j) {
            ans += (docset[j] == query.size());
        }
        printf("%d\n", ans);
    }
}

int main(int argc, char* argv[]) {
    freopen(argv[1], "r", stdin);
    freopen(argv[2], "w", stdout);
    loadData();
    work();
    return 0;
}
