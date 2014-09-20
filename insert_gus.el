; heavy inspiration taken from:
; http://ergoemacs.org/emacs/elisp_generate_uuid.html

(defun insert-gus-hash ()
  (interactive)
  "Insert a random 5 character hash (ex. 309ec) at point, for use with Globally
Unique Selector (GUS) syntax. Taken from an md5 hash of variable system data."
  (let ((myStr (substring
		(md5 (format "%s%s%s%s%s%s"
			     (emacs-pid)
			     (user-full-name)
			     (current-time)
			     (emacs-uptime)
			     (garbage-collect)
			     (random)))
		27 32)))
    (if (and (string-match-p "[0-9]" myStr)
	     (string-match-p "[a-f]" myStr))
	(insert myStr)
      (insert-gus-hash))))
