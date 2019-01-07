# imapfilter
## Simple filtering tool for moving junk mail to defined IMAP folder and deleting them

Just apply rules like th e follwing in apply_rules-function

```
move_by_header_field('From', 'ebay', "Mist")
move_by_header_field('From', 'cisco', "Mist")
move_by_header_field('From', 'cybrary', "Mist")
move_by_header_field('From', 'linuxacademy', "Mist")
move_by_header_field('Subject', 'Weihnachten', "Mist")
```


