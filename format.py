class Format:
    def clean(self, input):
        """
        >>> x = [(330,), (700,), (330,), (200,), (128,), (200,), (100,), (200,)]
        >>> Format().clean(x)
        [330, 700, 330, 200, 128, 200, 100, 200]

        >>> x = []
        >>> Format().clean(x)
        []
        """
        clean_array = []
        for row in input:
            clean_array.extend(row)
        return clean_array


if __name__ == "__main__":  # pragma: no cover
    import doctest
    doctest.testmod(verbose=2)
