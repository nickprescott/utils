; Lifted from: http://ergoemacs.org/emacs/elisp_generate_uuid.html
;;; by Christopher Wellons. 2011-11-18. Editted by Xah Lee.
;;; Edited by Hideki Saito further to generate all valid variants for "N"
;;; in xxxxxxxx-xxxx-Mxxx-Nxxx-xxxxxxxxxxxx format.

(defun np-insert-uuid-internal ()
  "Insert a UUID. This uses a simple hashing of variable data."
  (let ((myStr
	 (md5 (format "%s%s%s%s%s%s%s%s%s%s"
		      (user-uid)
		      (emacs-pid)
		      (system-name)
		      (user-full-name)
		      (current-time)
		      (emacs-uptime)
		      (garbage-collect)
		      (buffer-string)
		      (random)
		      (recent-keys)))))

    (format "%s-%s-4%s-%s%s-%s"
	    (substring myStr 0 8)
	    (substring myStr 8 12)
	    (substring myStr 13 16)
	    (format "%x" (+ 8 (random 4)))
	    (substring myStr 17 20)
	    (substring myStr 20 32))))

(defun np-is-valid-gus-id (var-string)
  (and (string-match-p "[0-9]" var-string)
       (string-match-p "[a-f]" var-string)))

(defun np-insert-gus ()
  "Insert a 5 character alphanumeric hash (ex. 62b57) at point"
  (interactive)
  (let ((subStr (substring (np-insert-uuid-internal) 31 36)))
    (if (np-is-valid-gus-id subStr)
	(insert subStr)
      (np-insert-gus))))
