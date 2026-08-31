package main

# 1. منع العمل كمستخدم root
deny[msg] {
    input[i].Cmd == "user"
    val := input[i].Value
    contains(val[0], "root")
    msg = "Security Policy Violation: Do not run container as root user."
}

# 2. التأكد من فتح المنفذ الصحيح للتطبيق
deny[msg] {
    not has_valid_expose
    msg = "Security Policy Violation: Container must expose port 5000."
}

has_valid_expose {
    input[i].Cmd == "expose"
    val := input[i].Value
    val[_] == "5000"
}
