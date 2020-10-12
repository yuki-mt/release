git filter-branch -f --env-filter \
  "GIT_AUTHOR_NAME='yuki-mt'; \
   GIT_AUTHOR_EMAIL='yuki1031mt@gmail.com'; \
   GIT_COMMITTER_NAME='yuki-mt'; \
   GIT_COMMITTER_EMAIL='yuki1031mt@gmail.com';" \
  HEAD~3..HEAD  # from the 3rd newest commit to the newest commit
