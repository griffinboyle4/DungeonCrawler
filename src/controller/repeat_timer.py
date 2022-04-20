from threading import Timer


class RepeatTimer(Timer):
    """This class represents a repeating timer to call a given callable."""
    daemon = True

    def run(self):
        """Calls the instance callable provided on initialization
        on every passing of the interval provided on initialization,
        until the cancel method is called.
        :return: None
        """
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)
